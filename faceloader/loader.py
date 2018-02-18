import logging
import face_recognition


def load_faces(data):
    faces = []
    linker = []
    nb_faces = 0

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
            except:
                logger.exception("message", exc_info=True)
                nb_faces = nb_faces - 1
                raise

        data[key]['hello'] = 0

    return faces, linker, nb_faces
