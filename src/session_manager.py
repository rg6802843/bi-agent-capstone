import os
from datetime import datetime
import json


class SessionManager:
    def __init__(self):

        # find project root
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # force absolute paths
        self.sessions_dir = os.path.join(self.project_root, "sessions")
        os.makedirs(self.sessions_dir, exist_ok=True)

    def create_session(self, file_path):
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = os.path.join(self.sessions_dir, session_id)
        os.makedirs(folder, exist_ok=True)

        meta = {
            "session_id": session_id,
            "file_path": file_path,
            "created_at": str(datetime.now()),
            "metrics": {},
        }

        with open(os.path.join(folder, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)

        return session_id

    def load_meta(self, session_id):
        path = os.path.join(self.sessions_dir, session_id, "meta.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_meta(self, session_id, meta):
        path = os.path.join(self.sessions_dir, session_id, "meta.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)
