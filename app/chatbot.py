# Handles user onboarding and collects data for the AI.

import openai

# openai.api_key = 'your-openai-api-key'

def get_user_data_conversation(user_input):
    """Interact with the user to collect necessary data for routine generation."""

    # Sample interactive questions based on previous input
    if 'addiction_type' not in user_input:
        return "What type of addiction are you struggling with?"

    elif 'struggles' not in user_input:
        return "What specific struggles have you faced trying to overcome this addiction?"

    elif 'goals' not in user_input:
        return "What are your goals for overcoming this addiction?"

    # If all data is collected, generate the routine
    else:
        return "Thank you for sharing, let's generate your personalized routine!"
