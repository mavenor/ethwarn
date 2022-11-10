import face_recognition as fr
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from time import time

img = fr.load_image_file("./foo.jpg")
encodings = fr.face_encodings(img)

stream = VideoCapture(0)
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
    
    
