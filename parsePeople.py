import os
import json


def loadData():
    baseDir = './people'
    people = os.listdir(baseDir)
    data = {}

    for person in people:
        if os.path.isdir(baseDir + '/' + person):
            if os.path.isfile(baseDir + '/' + person + '/info.json'):
                data[person] = json.load(open(baseDir + '/' + person + '/info.json'))
            else:
                name_tmp = person.split()
                data[person] = {'name': name_tmp[1] + ' ' + name_tmp[0], 'firstname': name_tmp[1], 'lastname': name_tmp[0]}
            data[person]['facesPath'] = [baseDir + '/' + person + '/face.jpg']

    return data
