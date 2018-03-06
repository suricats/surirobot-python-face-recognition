from threading import Thread
import os
import cv2
import face_recognition
import adapters
import shared as s


class FaceRecognition(Thread):
    def __init__(self):
        Thread.__init__(self)
        # Initialize adapters
        self.com = adapters.Communicator(['redis'])

    def run(self):

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
                    match = face_recognition.compare_faces(s.faces, face_encoding, tolerance)
                    name = "Unknown"

                    for key, value in enumerate(match):
                        if value:
                            name = s.data[s.linker[key]]['name']
                            break
                    face_names.append(name)

            process_this_frame = not process_this_frame
            self.com.process([frame, face_locations, face_names])

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
