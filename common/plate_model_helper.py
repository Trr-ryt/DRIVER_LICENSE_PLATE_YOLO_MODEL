from ultralytics import YOLO
import cv2
import numpy as np
import threading
from common.drv_lic_helper import ThaiLicenseHelper

class PlateModelHelper:
    def __init__(self, vehicle_rois: list, frame: np.ndarray):
        self.frame = frame
        self.plate_model: YOLO = YOLO("models/data_plate_ncnn_model")  # detect license plate
        self.detected_classes: list = []
        self.plates: list = []
        self.drv_lic_thai: ThaiLicenseHelper = ThaiLicenseHelper()
        self.vehicle_rois = vehicle_rois
        self.x1_offset: int = 0
        self.y1_offset: int = 0
        self.stopped = False
        self.thread = threading.Thread(target=self.model_plate_detection, daemon=True)
        self.thread.start()

    def process_license_plate_boxes(self, plate_results):
        """Process detected license plate boxes and return sorted plates."""
        self.plates.clear()  # Clear previous plates
        for plate in plate_results:
            for plate_box in plate.boxes:
                px1, py1, px2, py2 = map(int, plate_box.xyxy[0])
                px1, px2 = px1 + self.x1_offset, px2 + self.x1_offset
                py1, py2 = py1 + self.y1_offset, py2 + self.y1_offset
                self.plates.append((px1, plate_box.cls, (px1, py1, px2, py2)))
        self.plates.sort(key=lambda x: x[0])  # Sort plates by x1 coordinate

    def draw_license_plate_boxes(self):
        """Draw license plate boxes on the frame and update detected classes."""
        for plate in self.plates:
            px1, cls, (x1_plate, y1_plate, x2_plate, y2_plate) = plate
            cv2.rectangle(self.frame, (x1_plate, y1_plate), (x2_plate, y2_plate), (255, 255, 0), 2)  # Blue rectangle for plates
            clsname = self.plate_model.names[int(cls)]
            self.detected_classes.append(clsname)

    def arrange_detected_classes(self):
        """Arrange detected classes to prioritize provinces."""
        for item in self.detected_classes:
            if item in self.drv_lic_thai.PROVINCE_MAPPING:
                self.detected_classes.remove(item)
                self.detected_classes.append(item)

    def model_plate_detection(self):
        while not self.stopped:
            if self.frame is not None:
                self.detected_classes.clear()  # Clear previous detected classes
                # Detect license plates for each vehicle ROI
                for car_roi, x1, y1 in self.vehicle_rois:
                    plate_results = self.plate_model(car_roi, conf=0.3, verbose=False)
                    self.x1_offset, self.y1_offset = x1, y1
                    self.process_license_plate_boxes(plate_results)
                    self.draw_license_plate_boxes()

                # Arrange and process detected classes
                self.arrange_detected_classes()
                combined_text = "".join(self.drv_lic_thai.get_thai_character(newval) for newval in self.detected_classes)
                license_plate, province = self.drv_lic_thai.split_license_plate_and_province(combined_text)
                if license_plate is not None and province is not None:
                    drv_lic = f"ทะเบียนรถ:{license_plate} จังหวัด:{province}"
                    print(drv_lic)

    def plate_video(self) -> np.ndarray:
        """Return frame with detected license plates."""
        return self.frame.copy() if self.frame is not None else None

    def stop(self):
        """Stop the detection thread."""
        self.stopped = True
        self.thread.join()