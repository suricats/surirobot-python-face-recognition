import sys
import parsePeople
import face_recognition
import cv2
import threading
import speech
import logging
#import emotional
import redis

#Choose file name to load
fileNameFace = "face-640.jpg"
#fileNameFace = "face-ori.jpg"

#If you are getting multiple matches for the same person, 
#it might be that the people in your photos look very similar and a lower tolerance value is needed 
#to make face comparisons more strict. Default tolerance = 0.6
tolerance = 0.54 # if tolerance < 0.6 CI not recongnized

if (len(sys.argv) > 1):
    tolerance = sys.argv[1]
    
conn = redis.StrictRedis('172.16.69.10')

def publishToRedis(firstname):
    conn.publish('face-recognition', firstname)

faces = []
linker = []
nb_faces = 0
data = parsePeople.loadData(fileNameFace)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Start loading faces ....")
for key, person in data.items():
    for pic in person['facesPath']:
        logger.info("Load Face  ..... {}".format(person['facesPath']))
        img = face_recognition.load_image_file(pic)
        logger.info("        Face encoding .....")
        
        try:
            faces.append(face_recognition.face_encodings(img, None, 10)[0])
            linker.append(key)
            nb_faces = nb_faces + 1
        except :
            logger.exception("message", exc_info=True)
            nb_faces = nb_faces - 1
            raise
        
    data[key]['hello'] = 0

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    #cv2.imshow('img1',frame) #display the captured image
    #if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
    #    cv2.imwrite('images/c1.png',frame)
    #    cv2.destroyAllWindows()
    #    break
    #emotional.findemotional(frame)
    
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
                    data[linker[key]]['hello'] = (data[linker[key]]['hello'] + 1) % 70
                    if data[linker[key]]['hello'] == 7:
                        #threading.Thread(target=speech.say2, args=(data[linker[key]]['firstname'],)).start()
                        threading.Thread(target=publishToRedis, args=(data[linker[key]]['firstname'],)).start()
                        #conn.publish('face-recognition', data[linker[key]]['firstname'])
                    break
            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
