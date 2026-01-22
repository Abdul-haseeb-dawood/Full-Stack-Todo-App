from .add_task import add_task
from .read_tasks import read_tasks, read_task_by_id
from .update_task import update_task
from .delete_task import delete_task
from .complete_task import complete_task

# Define the tools available to the agent
TOOLS = {
    "add_task": add_task,
    "read_tasks": read_tasks,
    "read_task_by_id": read_task_by_id,
    "update_task": update_task,
    "delete_task": delete_task,
    "complete_task": complete_task
}

__all__ = [
    "add_task",
    "read_tasks", 
    "read_task_by_id",
    "update_task",
    "delete_task",
    "complete_task",
    "TOOLS"
]