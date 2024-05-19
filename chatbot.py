import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("No GROQ_API_KEY found in environment variables")

client = Groq(api_key=api_key)

# Function to get a response from the chatbot
def get_chat_response(user_input):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Main loop to interact with the chatbot
if __name__ == "__main__":
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = get_chat_response(user_input)
        print(f"Bot: {response}")
