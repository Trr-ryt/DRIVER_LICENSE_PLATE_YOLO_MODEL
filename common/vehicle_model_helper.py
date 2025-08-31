import threading
import torch
from ultralytics import YOLO
import numpy as np
import cv2
from common.drv_lic_helper import ThaiLicenseHelper
from common.__init__ import data_queue
class DetectVehicle:
    def __init__(self):
        self.frame = None
        try:
            self.vehicle_model: YOLO = YOLO("models/license_plate.pt").to("cuda" if torch.cuda.is_available() else "cpu")
            self.plate_model: YOLO = YOLO("models/data_plate.pt").to("cuda" if torch.cuda.is_available() else "cpu")
        except Exception as e:
            raise RuntimeError(f"Error loading YOLO models: {e}")

        self.vehicle_rois: list = []
        self.detected_classes: list = []
        self.plates: list = []
        self.drv_lic_thai: ThaiLicenseHelper = ThaiLicenseHelper()
        self.x1_offset: int = 0
        self.y1_offset: int = 0
        self.lock = threading.Lock()  # Threading lock for thread safety
        self.stopped = False
        self.thread = threading.Thread(target=self.model_vehicle_detection_process, daemon=True)
        self.thread.start()

    def process_license_plate_boxes(self, plate_results):
        """Process detected license plate boxes and return sorted plates."""
        self.plates.clear()  # Clear previous plates
        if not plate_results:
            return
        # Use list comprehension for efficiency
        plates = [
            (int(plate_box.xyxy[0][0]) + self.x1_offset, plate_box.cls,
             (int(plate_box.xyxy[0][0]) + self.x1_offset,
              int(plate_box.xyxy[0][1]) + self.y1_offset,
              int(plate_box.xyxy[0][2]) + self.x1_offset,
              int(plate_box.xyxy[0][3]) + self.y1_offset))
            for plate in plate_results for plate_box in plate.boxes
        ]
        plates.sort(key=lambda x: x[0])
        self.plates.extend(plates)

    def draw_license_plate_boxes(self):
        """Draw license plate boxes on the frame and update detected classes."""
        # Use set to avoid duplicate classes
        detected = set(self.detected_classes)
        for plate in self.plates:
            px1, cls, (x1_plate, y1_plate, x2_plate, y2_plate) = plate
            # Uncomment the next line to draw rectangles if needed
            # cv2.rectangle(self.frame, (x1_plate, y1_plate), (x2_plate, y2_plate), (255, 255, 0), 2)
            clsname = self.plate_model.names.get(int(cls), "Unknown")
            if clsname not in detected:
                self.detected_classes.append(clsname)
                detected.add(clsname)

    def arrange_detected_classes(self):
        """Arrange detected classes to prioritize provinces."""
        # Move all province items to the end, preserving order
        provinces = [item for item in self.detected_classes if item in self.drv_lic_thai.PROVINCE_MAPPING]
        others = [item for item in self.detected_classes if item not in self.drv_lic_thai.PROVINCE_MAPPING]
        self.detected_classes = others + provinces

    def process_vehicle_boxes(self, vehicle_results) -> None:
        """Process detected vehicle boxes and store ROIs."""
        with self.lock:  # Ensure thread safety
            if self.frame is None or not vehicle_results:
                return
            self.vehicle_rois.clear()  # Clear previous ROIs
            # Use list comprehension for efficiency
            self.vehicle_rois.extend([
                (self.frame[int(box.xyxy[0][1]):int(box.xyxy[0][3]), int(box.xyxy[0][0]):int(box.xyxy[0][2])],
                 int(box.xyxy[0][0]), int(box.xyxy[0][1]))
                for result in vehicle_results for box in result.boxes
            ])
    
    def model_detect_process(self):
        self.detected_classes.clear()  # Clear previous detected classes
        # Detect vehicles
        vehicle_results = self.vehicle_model(self.frame, conf=0.3, verbose=False)
        self.process_vehicle_boxes(vehicle_results)

        # Detect license plates for each vehicle ROI
        for car_roi, x1, y1 in self.vehicle_rois:
            plate_results = self.plate_model(car_roi, conf=0.3, verbose=False)
            self.x1_offset, self.y1_offset = x1, y1
            self.process_license_plate_boxes(plate_results)
            self.draw_license_plate_boxes()

        # Arrange and process detected classes
        self.arrange_detected_classes()
        # Use join only if detected_classes is not empty
        if self.detected_classes:
            combined_text = "".join(self.drv_lic_thai.get_thai_character(newval) for newval in self.detected_classes)
            license_plate, province = self.drv_lic_thai.split_license_plate_and_province(combined_text)
            if license_plate and province:
                print(f"ทะเบียนรถ: {license_plate} จังหวัด: {province}")
    
    def model_vehicle_detection_process(self):
        """Continuously detect vehicles in the frame."""
        while not self.stopped:
            if data_queue.empty() is False:
                self.frame = data_queue.get()
                self.model_detect_process()

    def vehicle_detection(self) -> np.ndarray:
        """Return the detected vehicle ROIs."""
        with self.lock:  # Ensure thread safety
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        """Stop the detection thread."""
        self.stopped = True
        self.thread.join()