import re
import asyncio
from typing import Dict, Any
from .gemini_client import get_gemini_client

async def get_gemini_response(prompt: str) -> str:
    """
    Get a response from the actual Gemini API based on the provided prompt.
    The function will use tools as needed to interact with the todo app.

    Args:
        prompt: The user's input/prompt

    Returns:
        The response as a string
    """
    try:
        # Get the current tasks to provide context to Gemini
        from .tools.read_tasks import read_tasks
        tasks_result = await read_tasks()
        context = None
        if tasks_result["success"]:
            context = {
                "available_tasks": [task["title"] for task in tasks_result["tasks"]],
                "total_tasks": len(tasks_result["tasks"])
            }

        # Get response from the actual Gemini API
        gemini_client = get_gemini_client()
        gemini_response = await gemini_client.generate_response(prompt, context)

        # Parse the response to determine if it's a command or general response
        if gemini_response.startswith("ACTION:"):
            # Parse the action from Gemini's response
            parts = gemini_response.split("|")
            action_dict = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    action_dict[key] = value

            action = action_dict.get("ACTION")

            if action == "add_task":
                title = action_dict.get("TITLE", "").strip('"\'')
                from .tools.add_task import add_task
                result = await add_task(title=title)
                if result["success"]:
                    return f"Okay, I've added \"{title}\" to your task list."
                else:
                    return f"Sorry, I couldn't add the task: {result['error']}"

            elif action == "update_task":
                old_title = action_dict.get("OLD_TITLE", "").strip('"\'')
                new_title = action_dict.get("NEW_TITLE", "").strip('"\'')

                # Find the task by title first
                from .tools.read_tasks import read_tasks
                read_result = await read_tasks()

                if read_result["success"]:
                    target_task = None
                    for task in read_result["tasks"]:
                        if task["title"].lower() == old_title.lower():
                            target_task = task
                            break

                    if target_task:
                        from .tools.update_task import update_task
                        update_result = await update_task(
                            task_id=target_task["id"],
                            title=new_title
                        )

                        if update_result["success"]:
                            return f"Okay, I've updated the task from '{old_title}' to '{new_title}'."
                        else:
                            return f"Sorry, I couldn't update the task: {update_result['error']}"
                    else:
                        return f"I couldn't find a task with the title '{old_title}'."
                else:
                    return f"Sorry, I couldn't retrieve your tasks to find the one to update: {read_result['error']}"

            elif action == "delete_task":
                title = action_dict.get("TITLE", "").strip('"\'')

                # Find the task by title first
                from .tools.read_tasks import read_tasks
                read_result = await read_tasks()

                if read_result["success"]:
                    target_task = None
                    for task in read_result["tasks"]:
                        if task["title"].lower() == title.lower():
                            target_task = task
                            break

                    if target_task:
                        from .tools.delete_task import delete_task
                        delete_result = await delete_task(task_id=target_task["id"])

                        if delete_result["success"]:
                            return f"Okay, I've deleted the task '{title}'."
                        else:
                            return f"Sorry, I couldn't delete the task: {delete_result['error']}"
                    else:
                        return f"I couldn't find a task with the title '{title}'."
                else:
                    return f"Sorry, I couldn't retrieve your tasks to find the one to delete: {read_result['error']}"

            elif action == "complete_task":
                title = action_dict.get("TITLE", "").strip('"\'')

                # Find the task by title first
                from .tools.read_tasks import read_tasks
                read_result = await read_tasks()

                if read_result["success"]:
                    target_task = None
                    for task in read_result["tasks"]:
                        if task["title"].lower() == title.lower():
                            target_task = task
                            break

                    if target_task:
                        from .tools.complete_task import complete_task
                        complete_result = await complete_task(task_id=target_task["id"])

                        if complete_result["success"]:
                            task_title = complete_result["task"]["title"]
                            new_status = "completed" if complete_result["task"]["completed"] else "marked as incomplete"
                            return f"Okay, I've {new_status} the task '{task_title}'."
                        else:
                            return f"Sorry, I couldn't update the task completion status: {complete_result['error']}"
                    else:
                        return f"I couldn't find a task with the title '{title}'."
                else:
                    return f"Sorry, I couldn't retrieve your tasks to find the one to mark as completed: {read_result['error']}"

            elif action == "list_tasks":
                if tasks_result["success"]:
                    if tasks_result["count"] == 0:
                        return "You don't have any tasks right now."
                    else:
                        task_list = "\n".join([f"- {task['title']}" for task in tasks_result["tasks"]])
                        return f"Here are your tasks:\n{task_list}"
                else:
                    return f"Sorry, I couldn't retrieve your tasks: {tasks_result['error']}"

            elif action == "general":
                return action_dict.get("RESPONSE", "I processed your request.")

            else:
                # If Gemini returned an unrecognized action, return its response directly
                return gemini_response
        else:
            # If Gemini didn't return an ACTION format, return its response directly
            return gemini_response

    except Exception as e:
        return f"Error processing request: {str(e)}"

if __name__ == "__main__":
    # Example usage
    user_input = "Add a new task: Buy groceries"
    response = asyncio.run(get_gemini_response(user_input))
    print(f"User: {user_input}")
    print(f"Assistant: {response}")