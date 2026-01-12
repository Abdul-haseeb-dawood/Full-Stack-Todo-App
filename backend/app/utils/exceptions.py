class TaskNotFoundException(Exception):
    """Raised when a task is not found in the database"""
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")


class TaskValidationException(Exception):
    """Raised when task validation fails"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)