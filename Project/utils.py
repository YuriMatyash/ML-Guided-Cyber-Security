import os
import json
import uuid
import threading
from datetime import datetime

from hyperparams import JSON_FILEPATH


# gets you the work ID as user input
def get_work_id() -> int:
    while True:
        try:
            WORK_ID = int(input("Write WORK_ID, int 1-100: "))
            if 1 <= WORK_ID <= 100:
                break
            else:
                print("Error: The number must be between 1 and 100.")   
        except ValueError:
            print("That's not a valid integer! Please try again.")  
    return WORK_ID


# Accepts an integer ID (1-100) and returns the corresponding base prompt string from the prompts_data.json
def get_base_prompt(prompt_id: int) -> str:

    # check if file exists
    if not os.path.exists(JSON_FILEPATH):
        return f"get_base_prompt({prompt_id}) Failed - Could not find json file at: {JSON_FILEPATH}"

    try:
        # load json
        with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
        
        str_id = str(prompt_id)
        
        # Structure: root -> "data" -> ID -> "original_prompt"
        if "data" in full_data and str_id in full_data["data"]:
            return full_data["data"][str_id]["original_prompt"]
        
        return f"Error: Prompt ID {prompt_id} not found in database."

    except json.JSONDecodeError:
        return "Error: Failed to decode JSON file."
    except Exception as e:
        return f"Error: {str(e)}"
    

# Adds a new mutated attack entry to the specified target ID in the JSON file
# Auto creates a unquie ID for the shift, can also update the parent id if it was provided.
# returns the new ID
def add_attack(target_id: int, shift_text: str, harmlessness_score: int = None, parent_id: str = None, response_text: str = "", response_metrics: dict = None) -> str:
    # generate unique ID
    new_shift_id = str(uuid.uuid4())
    str_id = str(target_id)
    
    # construct the metrics dictionaries
    prompt_metrics = {}
    if harmlessness_score is not None:
        prompt_metrics["harmlessness"] = harmlessness_score
    
    # Default to empty dict if None provided
    if response_metrics is None:
        response_metrics = {}

    # structure
    new_entry = {
        "shift_id": new_shift_id,
        "parent_id": parent_id,
        "shift_text": shift_text,
        "response": response_text,       # <--- Saved here
        "prompt_metrics": prompt_metrics,
        "response_metrics": response_metrics # <--- Saved here
    }

    with threading.Lock():
        # load data
        if os.path.exists(JSON_FILEPATH):
            try:
                with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
                    file_content = json.load(f)
            except json.JSONDecodeError:
                file_content = {"metadata": {}, "data": {}}
        else:
            file_content = {
                "metadata": {"source": "JailbreakBench", "version": "1.0"},
                "data": {}
            }

        # update data, ensure taget ID exists
        if str_id not in file_content["data"]:
            file_content["data"][str_id] = {
                "original_prompt": "Unknown Prompt (Auto-Created)",
                "category": "Unknown",
                "attacks": []
            }
        
        # write
        file_content["data"][str_id]["attacks"].append(new_entry)
        file_content["metadata"]["last_updated"] = datetime.now().isoformat()

        # save
        with open(JSON_FILEPATH, 'w', encoding='utf-8') as f:
            json.dump(file_content, f, indent=4)

    return new_shift_id


# Retrieves the shift_id of the attack with the highest harmlessness score for the given work_id
# if none exist returns None
def get_best_shift_id(work_id: int) -> str:
    if not os.path.exists(JSON_FILEPATH):
        print(f"Error: JSON file not found at {JSON_FILEPATH}")
        return None

    try:
        with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        str_id = str(work_id)
        
        # Check if work_id exists and has attacks
        if "data" not in data or str_id not in data["data"]:
            return None
        
        attacks = data["data"][str_id].get("attacks", [])
        if not attacks:
            return None

        # Find the attack with the highest score. 
        # We use .get() chain to default to -1 if metrics are missing.
        best_attack = min(
            attacks, 
            key=lambda x: x.get("prompt_metrics", {}).get("harmlessness", 101)
        )
        
        return best_attack["shift_id"]

    except Exception as e:
        print(f"Error finding best shift ID: {e}")
        return None


# retrieves the shift_text of a given work_id and shift_id
def get_shift_text(work_id: int, shift_id: str) -> str:
    if not os.path.exists(JSON_FILEPATH):
        return None

    try:
        with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        str_id = str(work_id)
        
        if "data" in data and str_id in data["data"]:
            attacks = data["data"][str_id]["attacks"]
            
            # Search for the matching shift_id
            for attack in attacks:
                if attack["shift_id"] == shift_id:
                    return attack["shift_text"]
                    
        return None

    except Exception as e:
        print(f"Error retrieving shift text: {e}")
        return None

