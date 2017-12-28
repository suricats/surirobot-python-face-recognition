import unittest
import json
from peopleparser import parsePeople
import pprint


class ParsePeopleTest(unittest.TestCase):

    """Testing the behavior of parsing people."""

    def test_parse(self):
        """Testing the behavior of parsing people."""

        res = parsePeople.loadData()
        expected_res = {
            "BERTRAND Loïc": {
                "name": "Loïc BERTRAND",
                "firstname": "Loïc",
                "lastname": "BERTRAND",
                "facesPath": [
                    "./people/BERTRAND Loïc/face-640.jpg"
                ]
            },
            "CECONI Annie-France": {
                "name": "Annie-France CECONI",
                "firstname": "Annie-France",
                "lastname": "CECONI",
                "facesPath": [
                    "./people/CECONI Annie-France/face-640.jpg"
                ]
            },
            "DUPONT Jean": {
                "name": "Jean DUPONT",
                "firstname": "Jean",
                "lastname": "DUPONT",
                "facesPath": [
                    "./people/DUPONT Jean/face-640.jpg"
                ]
            }
        }

        compare = (json.dumps(res, ensure_ascii=False) == json.dumps(expected_res, ensure_ascii=False))

        if not compare:
            print(json.dumps(res) + "\n\n is not equals to \n\n" + json.dumps(expected_res))

        self.assertTrue(compare)
