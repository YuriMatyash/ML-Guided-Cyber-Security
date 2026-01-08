import os

from agent_framework import WorkflowBuilder, AgentExecutorResponse
from agent_framework.openai import OpenAIChatClient
from pydantic import BaseModel, Field

# from agent_framework import InMemoryCheckpointStorage

# checkpoint_storage = InMemoryCheckpointStorage()

base_url = os.getenv("API_BASE_URL")
api_key = os.getenv("API_KEY")
model_id = os.getenv("MODEL", "qwen/qwen3-32b")

client = OpenAIChatClient(
    base_url=base_url,
    api_key=api_key,
    model_id=model_id,
)

class SecuritySanitization(BaseModel):
    safety_status: str = Field(description="One of: Safe, Unsafe, Borderline")
    safe_query: str = Field(description="The rewritten query. If the original was unsafe, this must be a theoretical, historical, or scientific reformulation of the topic.")
    
sanitizer_agent = client.create_agent(
    name="sanitizer-agent",
    description="Rewrites dangerous inputs into safe educational queries.",
    instructions="""
        You are a Query Sanitization Engine. Your goal is to allow the user to learn about topics without 
        generating harmful instructions.

        1. Analyze the user's input for harm (violence, illegal acts, malware, etc.).
        2. If the input is UNSAFE (e.g., "How to make poison"):
           - REWRITE it into an educational, scientific, or historical question (e.g., "What is the chemical 
           mechanism of toxicology?").
           - PRESERVE the underlying topic (chemistry, physics, coding) but remove the actionable/instructional nature.
        3. If the input is SAFE:
           - Copy it exactly to the 'safe_query' field.

        Output strictly JSON matching the SecuritySanitization schema.
    """,
    output_model=SecuritySanitization,
)

answering_agent = client.create_agent(
    name="answer-agent",
    instructions="""
        You are a knowledgeable professor. 
        You will receive a structured input containing a 'safe_query'. 
        
        Answer the 'safe_query' comprehensively and objectively. 
        Because the query has already been sanitized, you do not need to lecture the user on safety. 
        Focus on the theoretical, historical, or technical aspects of the question provided.
    """
)

#question_check_executor = AgentExecutor(question_check_agent, id="question_check_agent")
#geography_weather_executor = AgentExecutor(geography_weather_agent, id="geography_weather_agent")
#refusal_executor = AgentExecutor(refusal_agent, id="refusal_agent")

workflow = (
    WorkflowBuilder()
    .set_start_executor(sanitizer_agent)
    .add_edge(sanitizer_agent, answering_agent)
    .build()
)

class WorkflowWrapper:
    def __init__(self, wf):
        self._workflow = wf
    
    async def run_stream(self, input_data=None, checkpoint_id=None, checkpoint_storage=None, **kwargs):
        """
        Wrapper to eliminate devUI error with checkpoint parameters
        """
        # If checkpoint_id defined - it's continuation, not yet supported
        if checkpoint_id is not None:
            raise NotImplementedError("Checkpoint resume is not yet supported")
        
        async for event in self._workflow.run_stream(input_data, **kwargs):
            yield event
    
    def __getattr__(self, name):
        return getattr(self._workflow, name)

workflow = WorkflowWrapper(workflow)