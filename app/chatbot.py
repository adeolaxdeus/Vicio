def get_user_data_conversation(user_input):
    """Interact with the user to collect necessary data for routine generation."""
    
    # Check if this is the first interaction (i.e., no data has been collected yet)
    if 'addiction_type' not in user_input:
        user_input['addiction_type'] = None  # placeholder until the user responds
        return "What type of addiction are you struggling with?"

    elif 'addiction_type' in user_input and not user_input['addiction_type']:
        # Capture the response to the previous question and move forward
        user_input['addiction_type'] = user_input.get('user_message', '')
        return "What specific struggles have you faced trying to overcome this addiction?"

    elif 'struggles' not in user_input:
        return "What specific struggles have you faced trying to overcome this addiction?"

    elif 'goals' not in user_input:
        return "What are your goals for overcoming this addiction?"

    else:
        return "Thank you for sharing, let's generate your personalized routine!"
