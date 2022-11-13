import picamera2 as cam
from time import time
from face_recognition import face_encodings as encode, compare_faces, face_locations, load_image_file as imgread
from numpy import empty as newarr, uint8, NDArray

class facemon:
    # camera object
    camera: cam.Picamera2

    # face memory
    face0: NDArray

    # most recent frame containing a face
    # used when face has just been discovered using has_face()
    recent_positive_frame: NDArray

    def __init__(self):
        self.camera = cam.Picamera2()
        self.camera.still_configuration.main.size = (1296, 972)
        self.camera.configure("still")
        self.camera.start()
        self.recent_positive_frame = None

    # store most recent frame with face into face memory
    def store_face(self):
        if self.recent_positive_frame is None:
            self.recent_positive_frame = self.camera.capture_array("main")
        self.face0 = encode(self.recent_positive_frame)[0]

    # check if 
    def match_face(self):
        self.frame = self.camera.capture_array("main")
        face1 = encode(self.frame)[0]
        return compare_faces([self.face0], face1)

    # face is present in stream?
    def has_face(self) -> bool:
        start = time()
        total = 0
        positve = 0
        while (time() - start < 10):
            frame = self.camera.capture_array("main")
            # only one face should be in the frame
            if (len(face_locations(frame)) == 1):
                positve += 1
                self.recent_positive_frame = frame
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
