import os
import random
import cowsay
from typing import Annotated, Dict
from pydantic import Field
from agent_framework import ChatAgent, ai_function
from agent_framework.openai import OpenAIChatClient

# ---------------------------
#  Configuration
# ---------------------------
# We load these from the .env file for security
base_url = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
api_key = os.getenv("API_KEY")
model_id = os.getenv("MODEL", "google/gemini-2.0-flash-exp:free")

if not api_key:
    print("CRITICAL WARNING: API_KEY is missing. Check your .env file.")

# ---------------------------
#  The Random Art Tool
# ---------------------------

@ai_function(
    name="make_random_ascii_art",
    description="Takes a text string and returns it formatted as ASCII art using a random character.",
)
def make_random_ascii_art(
    message: Annotated[
        str, 
        Field(description="The English text for the character to say.")
    ]
) -> Dict:
    """
    Generates ASCII art of a random character saying the message.
    """
    valid_chars = cowsay.char_names
    random_char = random.choice(valid_chars)
    art = cowsay.get_output_string(random_char, message)
    
    return {
        "character_used": random_char,
        "art": art
    }

# ---------------------------
#  Client & Agent Setup
# ---------------------------

# Initialize the client with the new OpenRouter model
client = OpenAIChatClient(
    base_url=base_url,
    api_key=api_key,
    model_id=model_id,
)

agent = ChatAgent(
    chat_client=client,
    name="hebrew-random-art-translator",
    instructions="""
        You are a fun translator agent using the GPT-OSS-120b model.
        
        Your Workflow:
        1. Receive text from the user (usually in Hebrew).
        2. Translate that text into English.
        3. Use the tool 'make_random_ascii_art' with the English translation.
        
        Do not output the plain text translation. Only output the result of the tool.
    """,
    tools=[make_random_ascii_art],
)