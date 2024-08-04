from datetime import datetime, timedelta
from enum import Enum

class BotStatus:
    class Status(Enum):
        ONLINE = "online"
        RUNNING = "running"
        ERROR = "error"
        COMPLETE = "complete"

    def __init__(self):
        self.current_status = self.Status.ONLINE
        self.last_updated = datetime.now()
        self.status_history = []

    def set_status(self, new_status):
        try:
            new_status = self.Status(new_status.lower())
            self.status_history.append({
                "status": self.current_status,
                "changed_at": self.last_updated
            })
            self.current_status = new_status
            self.last_updated = datetime.now()
            return True
        except ValueError:
            return False

    def get_current_status(self):
        return self.current_status.value