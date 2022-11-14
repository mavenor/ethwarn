import picamera2 as cam
from time import time
from face_recognition import face_encodings as encode, face_distance as dist, face_locations
from numpy import ndarray
from statistics import mean


class facemon:
    # camera object
    camera: cam.Picamera2

    # face memory
    # (EMBEDDINGS)
    face0: list[ndarray]

    # most recent frame containing a face
    # used when face has just been discovered using has_face()
    # (RAW RGB DATA)
    recent_positive_frame: ndarray

    def __init__(self):
        self.camera = cam.Picamera2()
        self.camera.still_configuration.main.size = (640, 480)
        self.camera.still_configuration.main.format = "RGB888"
        self.camera.configure("still")
        self.camera.start()
        self.recent_positive_frame = []
        self.face0 = []

    # store most recent frame with face into face memory
    def store_face(self):
        if self.recent_positive_frame is None:
            self.wait_face()
        self.face0.append(encode(self.recent_positive_frame)[0])

    def init_face(self):
        for __ in range(5):
            frame = self.camera.capture_array("main")
            if len(face_locations(frame)) == 1:
                self.face0.append(encode(frame)[0])

    def reset_face(self):
        self.face0.clear()

    # check if 
    def match_face(self):
        # self.frame = self.camera.capture_array("main")
        distance = []
        for i in range(5):
            frame = self.camera.capture_array()
            if len(face_locations(frame)) == 1:
                face1 = encode(frame)[0]
                distance.append(dist(self.face0, face1))
        the_mean = mean([x.mean() for x in distance])
        print(f"match distance overall mean = {the_mean}")
        return (the_mean <= 0.4)

    # face is present in stream?
    def has_face(self) -> bool:
        start = time()
        positive = 0
        # while (time() - start < 6):
        for __ in range(5):
            frame = self.camera.capture_array("main")
            # only one face should be in the frame
            if (len(face_locations(frame)) == 1):
                positive += 1
                self.recent_positive_frame = frame
        # use smoothing for false positives
        print(f"checked for face, found {positive} of 6")
        return (float(positive)/5 >= 0.8)
        # frame = self.camera.capture_array()
        # if (len(face_locations(frame)) == 1):
        #     self.recent_positive_frame = frame
        #     return True
        # else:
        #     return False
        
    # wait for a face to appear
    def wait_face(self):
        while True:
            if self.has_face():
                break
        # face detected once outside loop
