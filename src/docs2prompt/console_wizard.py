from prompt_toolkit import prompt

def ai_response(user_input):
    # Placeholder function for AI response
    return f"AI expanded idea based on: '{user_input}'"

def role_chat():
    print("Let's refine your role definition.")

    # Example of interactive chat for defining AI role
    user_input = prompt("Provide a basic role description (e.g., 'python coder'): ")
    while True:
        response = ai_response(user_input)
        print(f"AI Response: {response}")

        # Ask for approval or comments for further refinement
        user_feedback = prompt("Do you approve this description? (yes/comment): ")

        if user_feedback.lower() == "yes":
            print("Role description approved.")
            break
        else:
            user_input = prompt("Provide your comments for improvement: ")

    return response

if __name__ == "__main__":
    role_chat()
