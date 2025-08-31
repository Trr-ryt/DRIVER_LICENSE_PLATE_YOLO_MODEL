import threading
import cv2
import numpy as np
from common.__init__ import data_queue
class VideoStream:
    def __init__(self, src: str = '', width: int = 1280, height: int = 720, fps: int = 30):
        self.cap = cv2.VideoCapture(src)
        self.width = width
        self.height = height
        self.fps = fps
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.ret, self.frame = self.cap.read()
        if self.ret:
            self.frame = cv2.resize(self.frame, (self.width, self.height))
        self.stopped = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while not self.stopped and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (self.width, self.height))
            with self.lock:
                self.ret = ret
                self.frame = frame
            data_queue.put(frame)

    def read(self) -> np.ndarray:
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            return None
    
    def stop(self):
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join()
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()