import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from datasets import load_dataset

JSON_FILEPATH = "Project/prompts_data.json"

# --- 1. Class Definition ---
class DataManager:
    def __init__(self, filepath: str = JSON_FILEPATH):
        self.filepath = filepath
        # Ensure the directory exists to prevent FileNotFoundError
        if os.path.dirname(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.data = self._load_data()

    ############################################################################################
    # Public Methods
    ############################################################################################
    
    # adds a new target prompt
    def register_target(self, jbb_id: str, original_prompt: str, category: str = "Unknown"):
        """
        Creates the bucket for a specific JBB ID (e.g., '1').
        """
        jbb_id = str(jbb_id)
        if jbb_id not in self.data["data"]:
            self.data["data"][jbb_id] = {
                "original_prompt": original_prompt,
                "category": category,
                "attacks": [] 
            }
            self._save_data()

    # returns attacks for a specific ID
    def get_attacks(self, jbb_id: str) -> List[Dict]:
        jbb_id = str(jbb_id)
        if jbb_id in self.data["data"]:
            return self.data["data"][jbb_id]["attacks"]
        return []
    
    # Updates a specific field for a specific attack
    def update_attack_field(self, jbb_id: str, shift_id: str, field: str, value):
        jbb_id = str(jbb_id)
        if jbb_id not in self.data["data"]:
            return False

        # Find the specific attack by shift_id
        attacks_list = self.data["data"][jbb_id]["attacks"]
        target_attack = None
        
        for attack in attacks_list:
            if attack["shift_id"] == shift_id:
                target_attack = attack
                break
        
        if not target_attack:
            return False

        # Mapping for Response Metrics (Standard HHH)
        response_metric_keys = ["helpful", "honest", "hopnet", "harmless", "total"]
        
        if field in response_metric_keys:
            # Handle the specific "hopnet" typo if it occurs
            key = "honest" if field == "hopnet" else field
            
            # Ensure the dict exists (just in case)
            if "response_metrics" not in target_attack:
                target_attack["response_metrics"] = {}
                
            target_attack["response_metrics"][key] = value

        # Handle explicit prompt_metrics updates if needed (e.g. field="prompt_metrics.helpful")
        elif "." in field:
            parent, child = field.split(".", 1)
            if parent in ["prompt_metrics", "response_metrics"]:
                if parent not in target_attack:
                    target_attack[parent] = {}
                target_attack[parent][child] = value

        # Top level fields (shift_text, response, parent_id, etc)
        else:
            target_attack[field] = value

        self._save_data()
        return True
    
    
    ##########################################################################################
    # Private Methods
    ##########################################################################################
    def _load_data(self) -> Dict:
        """Loads data or creates the skeleton."""
        if not os.path.exists(self.filepath):
            skeleton = {
                "metadata": {
                    "source": "JailbreakBench",
                    "version": "1.0", 
                    "created_at": datetime.now().isoformat()
                },
                "data": {}
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(skeleton, f, indent=4)
            return skeleton
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"metadata": {}, "data": {}}

    # saves data to from prompt
    def _save_data(self):
        """Saves data to disk."""
        self.data["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)