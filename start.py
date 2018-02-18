import os
import faceloader
import adapters
import face_recognition
import cv2
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Initialize adapters
com = adapters.Communicator(['redis'])
# Load faces
data = faceloader.parse_people(os.environ.get('FACERECO_IMG_NAME'))
faces, linker, nb_faces = faceloader.load_faces(data)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
tolerance = float(os.environ.get('FACERECO_TOLERANCE', '0.54'))

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        # num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations, 10)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(faces, face_encoding, tolerance)
            name = "Unknown"

            for key, value in enumerate(match):
                if value:
                    name = data[linker[key]]['name']
                    #data[linker[key]]['hello'] = (data[linker[key]]['hello'] + 1) % 70
                    #if data[linker[key]]['hello'] == 7:
                        #threading.Thread(target=speech.say2, args=(data[linker[key]]['firstname'],)).start()
                        #threading.Thread(target=publishToRedis, args=(data[linker[key]]['firstname'],)).start()
                        #conn.publish('face-recognition', data[linker[key]]['firstname'])
                    break
            face_names.append(name)

    process_this_frame = not process_this_frame
    com.process([frame, face_locations, face_names])

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
