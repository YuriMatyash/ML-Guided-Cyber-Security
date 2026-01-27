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
def add_attack(target_id: int, shift_text: str, parent_id: str = None) -> str:
    # generate unique ID
    new_shift_id = str(uuid.uuid4())
    str_id = str(target_id)
    
    # structure
    new_entry = {
        "shift_id": new_shift_id,
        "parent_id": parent_id,  # Updates if provided, else None
        "shift_text": shift_text,
        "response": "",
        "prompt_metrics": {},
        "response_metrics": {}
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
