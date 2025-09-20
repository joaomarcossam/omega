from dataclasses import dataclass
from consts import TaskStatus, Priority
from datetime import datetime

@dataclass
class Todo:
    title: str
    description: str
    due_date: datetime
    priority: Priority
    status: TaskStatus

    def __str__(self):
        return f"{self.title}: {self.due_date.strftime('%d/%m/%Y - %H:%M')}"
    