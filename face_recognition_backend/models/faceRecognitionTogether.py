from collections import Counter
from models.Facenet.face_recognition import run_face_recognition

def run_models(videoFile):
    nameList = []
    
    run_face_recognition(videoFile, nameList)
    
    if nameList:
        most_common_name = Counter(nameList).most_common(1)[0][0]
        print(f'Most common name: {most_common_name}')
        return most_common_name
    else:
        print('No names detected by facenet.')
        return "No face detected"