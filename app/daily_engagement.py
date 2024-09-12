#  This file handles task management, AI interaction for routine generation,
#  and daily task progression.

import openai

# openai.api_key = 'your-openai-api-key'

def generate_routine_with_ai(user_data):
    """Generates a routine using OpenAI's GPT API based on user input."""
    prompt = f"Create a daily routine to help someone overcome {user_data['addiction_type']} who struggles with {user_data['struggles']}."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )

    return response.choices[0].text.strip()

def extract_first_task(routine):
    """Extract the first task from the AI-generated routine."""
    tasks = routine.split('\n')
    return tasks[0] if tasks else "No tasks found."

def get_next_task(routine):
    """Get the next task based on the user's progress."""
    tasks = routine.full_routine.split('\n')
    current_index = tasks.index(routine.current_task)
    if current_index + 1 < len(tasks):
        return tasks[current_index + 1]
    return None