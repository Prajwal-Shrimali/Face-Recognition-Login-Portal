import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from models.faceRecognitionTogether import run_models
from flask_cors import CORS
from getUserData import getUserCredentials
from getUserLoginLink import getUserLoginLink
import os

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    frames = data.get('frames')

    frame_list = []
    for frame in frames:
        img_data = base64.b64decode(frame.split(',')[1])
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        frame_list.append(img)

    height, width, layers = frame_list[0].shape
    video_filename = 'captured_video.avi'
    video = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 10, (width, height))

    for frame in frame_list:
        video.write(frame)
    
    video.release()

    print(f"Received username: {username}")

    try:
        recognized_name = run_models(video_filename)
        print(f"Recognized name: {recognized_name}")
        
        if recognized_name == "No face detected":
            return jsonify({'message': 'No face detected, please try again.'}), 400
        
        if recognized_name == username:
            user_credentials = getUserCredentials(username=username)
            
            if user_credentials is None:
                return jsonify({'message': 'User credentials not found.'}), 404
            
            firstName, lastName, IAMUserName, accessToken, scecretAccessToken = user_credentials
            loginURL = getUserLoginLink(accessToken, scecretAccessToken, 'arn:aws:iam::864899838340:role/awsProjectUserRole')
            return jsonify({'message': f'Login successful for user: {username}', "firstName" : firstName, "lastName" : lastName, "IAMUserName" : IAMUserName, 'accessToken': accessToken, 'scecretAccessToken': scecretAccessToken, "loginURL" : loginURL}), 200
        else:
            return jsonify({'message': f'Face recognition failed for user: {username}. Recognized as: {recognized_name}'}), 403

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(video_filename):
            os.remove(video_filename)

if __name__ == '__main__':
    app.run(debug=True)
