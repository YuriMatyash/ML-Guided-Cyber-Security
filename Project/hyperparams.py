JSON_FILEPATH = "Project/prompts_data.json"
NUM_OF_ATTACKS = 5  # Attacks per iteration (per mutation round)
TOTAL_ATTACK_LIMIT = 200 # Global limit for the entire run

WORK_IDS = (47, 47)  # Define target IDs

MUTATOR_MODEL = "deepseek-r1:8b"
TARGET_MODEL = "qwen3:14b"
EVALUATOR_MODEL = "llama3.1:8b"