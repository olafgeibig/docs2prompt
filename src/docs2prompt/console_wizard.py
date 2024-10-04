from prompt_toolkit import prompt
from litellm import completion
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def ai_response(prompt):
    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are an AI assistant helping to refine input for an AI prompt generator. Expand on the user's input to create a more detailed input. Don't use markdown and variables"},
                {"role": "user", "content": f"{prompt}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in AI response: {e}")
        return f"Failed to get AI response. Using original input: '{prompt}'"

def role_chat():
    print("Let's refine your role definition.")

    # Example of interactive chat for defining AI role
    user_input = prompt("Provide a basic role description (e.g., 'python coder'): ")
    ai_prompt = f"Expand and improve this role description: {user_input}"
    while True:
        response = ai_response(ai_prompt)
        print(f"\nAI Response: {response}")

        # Ask for approval or comments for further refinement
        user_feedback = prompt("\nHow to proceed? approve(a), reject(r) or comment(c): ")

        if user_feedback.lower() == "a":
            print("\nRole description approved.")
            break
        elif user_feedback.lower() == "r":
            user_input = prompt("\nProvide a new basic role description (e.g., 'python coder'): ")
            ai_prompt = f"Expand and improve this role description: {user_input}"
        elif user_feedback.lower() == "c":
            comment = prompt("\nProvide your comments for improvement: ")
            ai_prompt = f"The user has change requests. The original request was {ai_prompt}\n\n your proposal was: {response}\n\nUser comments: {comment}"
        else:
            break

    return response

if __name__ == "__main__":
    role_chat()
