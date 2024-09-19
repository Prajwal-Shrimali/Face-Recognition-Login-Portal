from flask import Flask, request, jsonify
# from models.Facenet.face_recognition import run_face_recognition
from models.faceRecognitionTogether import run_models
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "*"}}) 

@app.route('/')
def index():
    return "Face Recognition Authentication Portal is running."

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Using get_json() to parse JSON data
    username = data.get('username')

    print(f"Received username: {username}")  # Debugging line to check received data

    try:
        # recognized_name = run_face_recognition()
        recognized_name = run_models()
        print(f"Recognized name: {recognized_name}")  # Debugging line to check recognized name
        
        if recognized_name == "No face detected":
            return jsonify({'message': 'No face detected, please try again.'}), 400
        
        if recognized_name == username:
            return jsonify({'message': f'Login successful for user: {username}'}), 200
        else:
            return jsonify({'message': f'Face recognition failed for user: {username}. Recognized as: {recognized_name}'}), 403

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
