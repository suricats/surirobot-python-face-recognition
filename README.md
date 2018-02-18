# python-face-recognition

[![Build Status](https://travis-ci.org/suricats/surirobot-python-face-recognition.svg?branch=master)](https://travis-ci.org/suricats/surirobot-python-face-recognition)

Recongize people from the webcam using a local library of people.
To add people, simply go in the folder 'people', create a new folder with the name of the person and drop a picture of it, named face.jpg

## Installation under macOS using homebrew

Install libs: `brew install python3 boost-python3 dlib`

Install required python3 modules: `pip3 install -r requirements.txt`

Install the lastest version of python3 dlib:

```bash
git clone https://github.com/davisking/dlib.git
cd dlib
python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no DLIB_USE_CUDA
cd .. && rm -rf dlib
```


## Get the suricats face pack

```bash
cp .env.example .env
nano .env
```

Fill the login & password fields

```bash
tools/get-people-data.sh
```

## Launch the program

`cd <project_dir>`

`python3 start.py`
