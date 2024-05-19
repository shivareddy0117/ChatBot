import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient, errors
import gridfs
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv
import json
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize MongoDB client and GridFS
mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = mongo_client['job_applications']
applications_collection = db['applications']
fs = gridfs.GridFS(db)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}

@app.route('/')
def index():
    return render_template('index5.html')

@app.route('/apply', methods=['POST'])
def apply():
    try:
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename == '':
                return jsonify({'message': 'No selected file. Please upload your resume.', 'next_state': 'resume', 'application_data': {}}), 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_id = fs.put(file, filename=filename)
                application_data = {'resume_file_id': str(file_id), 'resume_filename': filename}
                return jsonify({'message': 'Resume uploaded successfully. What is your first name?', 'next_state': 'first_name', 'application_data': application_data})
            else:
                return jsonify({'message': 'Invalid file type. Please upload a PDF, DOC, or DOCX file.', 'next_state': 'resume', 'application_data': {}}), 400
        else:
            data = request.get_json()
            state = data.get('state', 'resume')
            user_input = data.get('message', '')
            application_data = json.loads(data.get('application_data', '{}'))

            if state == "first_name":
                application_data['first_name'] = user_input
                return jsonify({'message': 'Thank you. What is your last name?', 'next_state': 'last_name', 'application_data': application_data})
            
            elif state == "last_name":
                application_data['last_name'] = user_input
                return jsonify({'message': 'What is your address?', 'next_state': 'address', 'application_data': application_data})
            
            elif state == "address":
                application_data['address'] = user_input
                return jsonify({'message': 'What is your phone number?', 'next_state': 'phone', 'application_data': application_data})
            
            elif state == "phone":
                application_data['phone'] = user_input
                return jsonify({'message': 'Are you authorized to work in the USA?', 'next_state': 'work_authorization', 'application_data': application_data})
            
            elif state == "work_authorization":
                application_data['work_authorization'] = user_input
                return jsonify({'message': 'What is your visa status?', 'next_state': 'visa_status', 'application_data': application_data})
            
            elif state == "visa_status":
                application_data['visa_status'] = user_input
                # Save all collected data to the database
                applications_collection.insert_one(application_data)
                return jsonify({'message': 'Application submitted successfully', 'next_state': 'done', 'application_data': {}})
            
            return jsonify({'message': 'Welcome to the job application chatbot. Please upload your resume.', 'next_state': 'resume', 'application_data': {}})
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@app.route('/history', methods=['GET'])
def history():
    try:
        history = list(applications_collection.find({}, {'_id': 0}))
        for record in history:
            if 'resume_file_id' in record:
                record['resume_url'] = f"/resume/{record['resume_file_id']}"
        return jsonify(history)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@app.route('/resume/<file_id>', methods=['GET'])
def get_resume(file_id):
    try:
        file = fs.get(ObjectId(file_id))
        response = app.response_class(file.read(), mimetype='application/octet-stream')
        response.headers.set('Content-Disposition', 'attachment', filename=file.filename)
        return response
    except errors.NoFile:
        return jsonify({'message': 'File not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
