import json
import os

class ProgressStore:
    def __init__(self, user_id="default_user"):
        # Store in the memory directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, f"{user_id}_progress.json")
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except:
                return self._default_structure()
        return self._default_structure()

    def _default_structure(self):
        return {
            "language": "Python", # Default to Python but allow change
            "level": None,
            "strengths": [],
            "weak_topics": [],
            "learning_path": {},
            "current_day": 1,
            "completed_days": [],
            "quiz_scores": []
        }

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def set_language(self, language):
        self.data["language"] = language
        self.save()
        
    def get_language(self):
        return self.data.get("language", "Python")

    def update_assessment(self, level, strengths, weaknesses):
        self.data["level"] = level
        self.data["strengths"] = strengths
        self.data["weak_topics"] = weaknesses
        self.save()

    def save_learning_path(self, path):
        self.data["learning_path"] = path
        self.save()
        
    def get_learning_path(self):
        return self.data.get("learning_path", {})

    def get_day_plan(self, day_number):
        key = f"day_{day_number}"
        return self.data.get("learning_path", {}).get(key, {})

    def mark_day_complete(self, day_number):
        if day_number not in self.data["completed_days"]:
            self.data["completed_days"].append(day_number)
            self.save()

    def add_quiz_score(self, day, topic, score):
        self.data["quiz_scores"].append({"day": day, "topic": topic, "score": score})
        self.save()
        
    def get_user_level(self):
        return self.data.get("level", None) # Changed default to None to force assessment
