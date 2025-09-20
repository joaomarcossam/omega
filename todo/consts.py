from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TaskStatus(IntEnum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3

    def __str__(self):
        return self.name.replace('_', ' ').title()