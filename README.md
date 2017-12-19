# python-face-recognition

Recongize people from the webcam using a local library of people.
To add people, simply go in the folder 'people', create a new folder with the name of the person and drop a picture of it, named face.jpg

## Installation under macOS using homebrew

Install python3 : brew install python3
Install boost-python : brew install boost-python --with-python3 --without-python
Install dlib : brew install dlib

Install required python3 modules : pip3 install opencv-python face_recognition gTTS

If error :
		ImportError: dlopen(/usr/local/lib/python3.6/site-packages/dlib/dlib.so, 
		2): Library not loaded: /usr/local/opt/boost-python/lib/libboost_python-mt.dylib   
		Referenced from: /usr/local/lib/python3.6/site-packages/dlib/dlib.so   
		Reason: image not found
		
cd /usr/local/Cellar/boost-python/1.65.1/lib/
ln -s libboost_python3-mt.dylib libboost_python-mt.dylib

## Launch the program

cd <project_dir>
python3 start.py

manifeste netflix
crapaud fou
management tribal
liberte et compagnie
