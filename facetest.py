import picamera
from time import time
from face_recognition import face_encodings as encode, compare_faces, face_locations, load_image_file as imgread
from numpy import empty as newarr, uint8, NDArray


img = imgread("./foo.jpg")
encodings = face_encodings(img)

camera = picamera.PiCamera()
camera.resolution = (1296, 972)
start = time()
while (time() - start < 20):
    __, frame = stream.read()
    rgb_frame = cvtColor(frame, COLOR_BGR2RGB)
    if (len(fr.face_locations(rgb_frame)) != 1):
        print("----------")
    else:
        if (fr.compare_faces([encodings], fr.face_encodings(rgb_frame)[0])):
            print("--**********--")
        else:
            print("---")
    
    
