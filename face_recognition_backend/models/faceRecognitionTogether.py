import threading
from collections import Counter
from models.Facenet.face_recognition import run_face_recognition
from models.CNN.testing import run_cnn_model

def run_models():
    nameList = []
    
    thread1 = threading.Thread(target=run_face_recognition, args=(nameList,))
    thread2 = threading.Thread(target=run_cnn_model, args=(nameList,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Return the most common name from nameList
    if nameList:
        most_common_name = Counter(nameList).most_common(1)[0][0]
        print(f'Most common name: {most_common_name}')
        return most_common_name
    else:
        print('No names detected.')
        return "No face detected"