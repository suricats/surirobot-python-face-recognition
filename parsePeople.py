import os
import json


def loadData(fileNameFace = "face-640.jpg"):
    baseDir = './people'
    people = os.listdir(baseDir)
    data = {}

    for person in people:
        if os.path.isdir(baseDir + '/' + person):
            if os.path.isfile(baseDir + '/' + person + '/info.json'):
                #Set encoding to utf-8 to open file with french characters
                data[person] = json.load(open(baseDir + '/' + person + '/info.json', encoding='utf-8'))
            else:
                name_tmp = person.split()
                data[person] = {'name': name_tmp[1] + ' ' + name_tmp[0], 'firstname': name_tmp[1], 'lastname': name_tmp[0]}
            data[person]['facesPath'] = [baseDir + '/' + person + '/' + fileNameFace]

    return data
