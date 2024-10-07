from prompt_toolkit import prompt
from litellm import completion
from dotenv import load_dotenv
from docs2prompt.arize_phoenix import openai_instrumentation

def ai_response(prompt, system_message):
    try:
        response = completion(
            # model="openrouter/deepseek/deepseek-chat",
            # model = "openrouter/qwen/qwen-2.5-72b-instruct",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e: 
        print(f"Error in AI response: {e}")
        return f"Failed to get AI response. Using original input: '{prompt}'"

def create_chat(chat_type):
    system_messages = {
        "role": "You are an AI assistant helping to create AI role descriptions for an AI prompt generator. Create a detailed and specific role description based on the user's input. Don't use markdown at all cost. Be brief and concise. Maximum 6 sentences.",
        "purpose": "You are an AI assistant helping to create project purpose for an AI prompt generator. Create a detailed and specific project purpose based on the user's input.",
        "instructions": "You are an AI assistant helping to create instructions for an AI prompt generator. Create detailed and specific instructions based on the user's input."
    }

    user_input = prompt(f"Provide a basic {chat_type} description: ")
    ai_prompt = f"Create a detailed {chat_type} description based on: {user_input}"
    return ai_response(ai_prompt, system_messages[chat_type])

def refine_chat(chat_type, current_content):
    system_messages = {
        "role": "You are an AI assistant helping to refine AI role descriptions for an AI prompt generator. Improve the existing role description based on the user's feedback. Don't use markdown at all cost. Be brief and concise. Maximum 6 sentences.",
        "purpose": "You are an AI assistant helping to refine project purposes for an AI prompt generator. Improve the existing project purpose based on the user's feedback.",
        "instructions": "You are an AI assistant helping to refine instructions for an AI prompt generator. Improve the existing instructions based on the user's feedback."
    }

    user_feedback = prompt("\nProvide your feedback for improvement: ")
    ai_prompt = f"Refine this {chat_type} description: {current_content}\n\nBased on this feedback: {user_feedback}"
    return ai_response(ai_prompt, system_messages[chat_type])

def interactive_chat(chat_type, initial_content=None):
    print(f"Let's {'refine' if initial_content else 'create'} your {chat_type} definition.")

    current_content = initial_content or create_chat(chat_type)

    while True:
        print(f"\n{current_content}")

        user_action = prompt("\nHow to proceed? approve(a), reject(r) or refine(f): ")

        if user_action.lower() == "a":
            print(f"\n{chat_type.capitalize()} description approved.")
            return current_content
        elif user_action.lower() == "r":
            current_content = create_chat(chat_type)
        elif user_action.lower() == "f":
            current_content = refine_chat(chat_type, current_content)
        else:
            print("Invalid input. Please try again.")

def wizard(chat_type, initial_content=None):
    return interactive_chat(chat_type, initial_content)

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    openai_instrumentation()

    print("Role Chat:")
    role_result = wizard("role")
    print("\nPurpose Chat:")
    purpose_result = wizard("purpose")
    print("\nInstructions Chat:")
    instructions_result = wizard("instructions")

    print("\nFinal Results:")
    print(f"Role: {role_result}")
    print(f"Purpose: {purpose_result}")
    print(f"Instructions: {instructions_result}")

    # Example of refining existing content
    print("\nRefining existing role:")
    refined_role = wizard("role", role_result)
    print(f"Refined Role: {refined_role}")
