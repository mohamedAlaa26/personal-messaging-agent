import json
import os

class ShortTermMemory:
    def __init__(self, max_len=10):
        self.max_len = max_len
        # Save memory.json in the project root folder (one level up from core)
        self.file_path = os.path.join(os.path.dirname(__file__), '../memory.json')
        self.histories = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_memory(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.histories, f, ensure_ascii=False, indent=2)

    def add_message(self, user_id, role, content):
        if user_id not in self.histories:
            self.histories[user_id] = []
        
        self.histories[user_id].append({"role": role, "content": content})
        
        # Keep only the last max_len messages
        if len(self.histories[user_id]) > self.max_len:
            self.histories[user_id] = self.histories[user_id][-self.max_len:]
        
        self._save_memory()

    def get_history(self, user_id):
        return self.histories.get(user_id, [])

    def clear_history(self, user_id):
        if user_id in self.histories:
            del self.histories[user_id]
            self._save_memory()