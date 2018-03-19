
from dotenv import load_dotenv, find_dotenv
import shared as s

# Load .env
load_dotenv(find_dotenv())

# Load global variables
s.init()

from recognition_engine.recognition import FaceRecognition
thread = FaceRecognition()
thread.start()

# Init from DB
from management.faceloader.loader import load_faces
load_faces()

# Launch Flask
from management import app

app.run(debug=False)
