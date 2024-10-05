from prompt_toolkit import prompt
from litellm import completion
from dotenv import load_dotenv
from docs2prompt.arize_phoenix import openai_instrumentation

# Load environment variables from .env file
load_dotenv()
openai_instrumentation()

def ai_response(prompt, system_message):
    try:
        response = completion(
            # model="gemini/gemini-1.5-flash",
            # model="gpt-3.5-turbo",
            model = "openrouter/deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e: 
        print(f"Error in AI response: {e}")
        return f"Failed to get AI response. Using original input: '{prompt}'"

def interactive_chat(chat_type):
    system_messages = {
        "role": "You are an AI assistant helping to refine AI role descriptions for an AI prompt generator. Expand on the user's input to create a more detailed and specific role description. Don't use markdown.",
        "purpose": "You are an AI assistant helping to refine project purposes for an AI prompt generator. Expand on the user's input to create a more detailed and specific project purpose.",
        "instructions": "You are an AI assistant helping to refine instructions for an AI prompt generator. Expand on the user's input to create more detailed and specific instructions."
    }

    print(f"Let's refine your {chat_type} definition.")

    user_input = prompt(f"Provide a basic {chat_type} description: ")
    ai_prompt = f"Expand and improve this {chat_type} description: {user_input}"

    while True:
        response = ai_response(ai_prompt, system_messages[chat_type])
        print(f"\n{response}")

        user_feedback = prompt("\nHow to proceed? approve(a), reject(r) or comment(c): ")

        if user_feedback.lower() == "a":
            print(f"\n{chat_type.capitalize()} description approved.")
            return response
        elif user_feedback.lower() == "r":
            user_input = prompt(f"\nProvide a new basic {chat_type} description: ")
            ai_prompt = f"Expand and improve this {chat_type} description: {user_input}"
        elif user_feedback.lower() == "c":
            comment = prompt("\nProvide your comments for improvement: ")
            ai_prompt = f"The user has change requests. The original request was: {ai_prompt}\n\nYour proposal was: {response}\n\nUser comments: {comment}"
        else:
            print("Invalid input. Please try again.")

def role_chat():
    return interactive_chat("role")

def purpose_chat():
    return interactive_chat("purpose")

def instructions_chat():
    return interactive_chat("instructions")

if __name__ == "__main__":
    print("Role Chat:")
    role_result = role_chat()
    print("\nPurpose Chat:")
    purpose_result = purpose_chat()
    print("\nInstructions Chat:")
    instructions_result = instructions_chat()

    print("\nFinal Results:")
    print(f"Role: {role_result}")
    print(f"Purpose: {purpose_result}")
    print(f"Instructions: {instructions_result}")
