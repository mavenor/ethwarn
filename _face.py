import picamera2 as cam
from time import time
from face_recognition import face_encodings as encode, face_distance as dist, face_locations, load_image_file as imgread
from numpy import empty as newarr, uint8, NDArray


class facemon:
    # camera object
    camera: cam.Picamera2

    # face memory
    # (EMBEDDINGS)
    face0: list[NDArray]

    # most recent frame containing a face
    # used when face has just been discovered using has_face()
    # (RAW RGB DATA)
    recent_positive_frame: NDArray

    def __init__(self):
        self.camera = cam.Picamera2()
        self.camera.still_configuration.main.size = (1296, 972)
        self.camera.still_configuration.main.format = "RGB888"
        self.camera.configure("still")
        self.camera.start()
        self.recent_positive_frame = None
        self.face0 = None

    # store most recent frame with face into face memory
    def store_face(self):
        if self.recent_positive_frame is None:
            self.wait_face()
        self.face0.append(encode(self.recent_positive_frame)[0])

    def reset_face(self):
        self.face0.clear()

    # check if 
    def match_face(self):
        self.frame = self.camera.capture_array("main")
        face1 = encode(self.frame)[0]
        distance = dist(self.face0, face1)
        return (distance.mean() >= 0.4)

    # face is present in stream?
    def has_face(self) -> bool:
        start = time()
        total = 0
        positve = 0
        while (time() - start < 6):
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
