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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_chat_response(user_input)

    # Store chat history in MongoDB
    chat_collection.insert_one({
        'user_message': user_input,
        'bot_response': response
    })

    return jsonify({'response': response})

@app.route('/history', methods=['GET'])
def history():
    history = list(chat_collection.find({}, {'_id': 0}))
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
