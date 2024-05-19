import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("No GROQ_API_KEY found in environment variables")

client = Groq(api_key=api_key)

# Initialize MongoDB client
mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = mongo_client['chatdb']
chat_collection = db['chathistory']

# Placeholder functions for banking services
def get_fico_score():
    return "Your FICO score is 750."

def get_bank_balance():
    return "Your bank balance is $10,000."

def get_customer_representative_number():
    return "You can reach a customer representative at 1-800-123-4567."

def get_chat_response(user_input, conversation_state):
    if conversation_state == "main_menu":
        return ("Hello! How can I assist you today? Please choose an option:\n1. Check FICO score\n2. Check bank balance\n3. Get customer representative number", "main_menu")
    elif conversation_state == "fico_score":
        return (get_fico_score(), "main_menu")
    elif conversation_state == "bank_balance":
        return (get_bank_balance(), "main_menu")
    elif conversation_state == "customer_representative":
        return (get_customer_representative_number(), "main_menu")
    else:
        return ("I'm not sure how to handle that. Please choose an option:\n1. Check FICO score\n2. Check bank balance\n3. Get customer representative number", "main_menu")

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    conversation_state = request.json.get('state', 'main_menu')

    # Determine the next state based on user input
    if conversation_state == "main_menu":
        if user_input == "1":
            new_state = "fico_score"
        elif user_input == "2":
            new_state = "bank_balance"
        elif user_input == "3":
            new_state = "customer_representative"
        else:
            new_state = "main_menu"
    else:
        new_state = "main_menu"

    response, new_state = get_chat_response(user_input, new_state)

    # Store chat history in MongoDB
    chat_collection.insert_one({
        'user_message': user_input,
        'bot_response': response,
        'state': new_state
    })

    return jsonify({'response': response, 'state': new_state})

@app.route('/history', methods=['GET'])
def history():
    history = list(chat_collection.find({}, {'_id': 0}))
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
