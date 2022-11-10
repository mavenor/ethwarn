import picamera
from time import time
from face_recognition import face_encodings as encode, compare_faces, face_locations, load_image_file as imgread
from numpy import empty as newarr, uint8, NDArray

class facemon:
    # face memory
    face0: NDArray

    camera = picamera.PiCamera()
    camera.resolution = (320, 240)

    # most recent frame containing a face
    # used when face has just been discovered using has_face()
    recent_positive_frame: NDArray

    frame = newarr((240, 320, 3), dtype=uint8)

    # store most recent frame with face into face memory
    def store_face(self):
        self.face0 = encode(self.recent_positive_frame)[0]

    # check if 
    def match_face(self):
        self.camera.capture(self.frame, format="rgb")
        face1 = encode(self.frame)[0]
        return compare_faces([self.face0], face1)

    # face is present in stream?
    def has_face(self):
        start = time()
        total = 0
        positve = 0
        while (time() - start < 10):
            if (len(face_locations(self.frame)) == 1):
                positve += 1
        total += 1

        # use smoothing for false positives
        return (float(positve)/float(total) >= 0.1)
        
    # wait for a face to appear
    def wait_face(self):
        while True:
            if self.has_face():
                break
        # face detected once outside loop


def single_face(image):
    img = imgread(image)
    return encode(img)[0]

def is_match(img1, img2):
    face1 = single_face(img1)
    face2 = single_face(img2)
    return compare_faces([face1], face2)
