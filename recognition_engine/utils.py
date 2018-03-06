import face_recognition

import shared as s


def add_picture(picture):
    if picture.user.id in s.data:
        pass
    else:
        s.data[picture.user.id] = {'name': picture.user.firstname + ' ' + picture.user.lastname, 'firstname': picture.user.firstname, 'lastname': picture.user.lastname}

    img = face_recognition.load_image_file(picture.path)
    face = face_recognition.face_encodings(img, None, 10)[0]

    s.faces.append(face)
    s.linker.append(picture.user.id)


def remove_picture(picture):
    key = s.linker.index(picture.user.id)
    del s.faces[key]
    del s.linker[key]
