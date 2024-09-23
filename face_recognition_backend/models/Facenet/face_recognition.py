from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
import numpy as np
from . import facenet
from . import detect_face
import os
import time
import pickle
from PIL import Image
import tensorflow.compat.v1 as tf
from collections import Counter

def run_face_recognition(video_path, recognized_list):
    modeldir = './models/Facenet/model/20180402-114759.pb'
    classifier_filename = './models/Facenet/class/classifier.pkl'
    npy = './models/Facenet/npy'
    train_img = "./models/Facenet/train_img"
    
    recognized_names = []

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)
            minsize = 30
            threshold = [0.7, 0.8, 0.8]
            factor = 0.709
            margin = 44
            batch_size = 100
            image_size = 182
            input_image_size = 160
            HumanNames = os.listdir(train_img)
            HumanNames.sort()
            print('Loading Model')
            facenet.load_model(modeldir)
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]
            classifier_filename_exp = os.path.expanduser(classifier_filename)
            with open(classifier_filename_exp, 'rb') as infile:
                (model, class_names) = pickle.load(infile, encoding='latin1')

            # Open the video file created from images
            video_capture = cv2.VideoCapture(video_path)

            print('Start Recognition')
            start_time = time.time()

            while time.time() - start_time < 10:  # Example duration to process the video
                ret, frame = video_capture.read()
                if not ret:
                    break

                if frame.ndim == 2:
                    frame = facenet.to_rgb(frame)
                bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                faceNum = bounding_boxes.shape[0]

                if faceNum > 0:
                    det = bounding_boxes[:, 0:4]
                    img_size = np.asarray(frame.shape)[0:2]
                    cropped = []
                    scaled = []
                    scaled_reshape = []

                    for i in range(faceNum):
                        emb_array = np.zeros((1, embedding_size))
                        xmin = int(det[i][0])
                        ymin = int(det[i][1])
                        xmax = int(det[i][2])
                        ymax = int(det[i][3])

                        try:
                            if xmin <= 0 or ymin <= 0 or xmax >= len(frame[0]) or ymax >= len(frame):
                                print('Face is very close!')
                                continue

                            cropped.append(frame[ymin:ymax, xmin:xmax, :])
                            cropped[i] = facenet.flip(cropped[i], False)
                            scaled.append(np.array(Image.fromarray(cropped[i]).resize((image_size, image_size))))
                            scaled[i] = cv2.resize(scaled[i], (input_image_size, input_image_size),
                                                    interpolation=cv2.INTER_CUBIC)
                            scaled[i] = facenet.prewhiten(scaled[i])
                            scaled_reshape.append(scaled[i].reshape(-1, input_image_size, input_image_size, 3))
                            feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                            emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)

                            predictions = model.predict_proba(emb_array)
                            best_class_indices = np.argmax(predictions, axis=1)
                            best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

                            if best_class_probabilities > 0.87:
                                recognized_names.append(HumanNames[best_class_indices[0]])
                                print(f"Predictions: [ name: {HumanNames[best_class_indices[0]]}, accuracy: {best_class_probabilities[0]:.3f}]")

                        except Exception as e:
                            print(f"Error processing frame: {str(e)}")

            # End processing
            video_capture.release()
            cv2.destroyAllWindows()

            if recognized_names:
                most_common_name = Counter(recognized_names).most_common(1)[0][0]
                print(f"Most common recognized name: {most_common_name}")
                recognized_list.append(most_common_name)
                return most_common_name
            else:
                print("No face detected")
                recognized_list.append("No face detected")
                return "No face detected"
