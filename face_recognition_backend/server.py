import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from models.faceRecognitionTogether import run_models
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    frames = data.get('frames')

    # Decode base64 frames and create a video
    frame_list = []
    for frame in frames:
        # Convert base64 image to OpenCV format
        img_data = base64.b64decode(frame.split(',')[1])
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        frame_list.append(img)

    # Save frames as video
    height, width, layers = frame_list[0].shape
    video_filename = 'captured_video.avi'
    video = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 10, (width, height))

    for frame in frame_list:
        video.write(frame)
    
    video.release()

    # return jsonify({'message': f'Video created for user: {username}', 'video': video_filename})
    print(f"Received username: {username}")  # Debugging line to check received data
    try:
        recognized_name = run_models(video_filename)
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
