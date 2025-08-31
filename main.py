import torch
import cv2
from ultralytics import YOLO

from common.drv_lic_helper import ThaiLicenseHelper
if torch.cuda.is_available():
    device = 'cuda'
    name = torch.cuda.get_device_name(torch.cuda.current_device())
else:
    device = 'cpu'
    name = 'CPU'
print(f"Using device: {name}, CUDA version: {torch.version.cuda}")

vehicle_model = YOLO("models/license_plate.pt").to(device)  # detect vehicle
plate_model = YOLO("models/data_plate.pt").to(device)  # detect license plate

def process_vehicle_boxes(vehicle_results, frame):
    """Process detected vehicle boxes and return cropped ROIs for license plate detection."""
    vehicle_rois = []
    for result in vehicle_results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle for vehicles
            car_roi = frame[y1:y2, x1:x2]
            vehicle_rois.append((car_roi, x1, y1))
    return vehicle_rois

def process_license_plate_boxes(plate_results, x1_offset, y1_offset):
    """Process detected license plate boxes and return sorted plates."""
    plates = []
    for plate in plate_results:
        for plate_box in plate.boxes:
            px1, py1, px2, py2 = map(int, plate_box.xyxy[0])
            px1, px2 = px1 + x1_offset, px2 + x1_offset
            py1, py2 = py1 + y1_offset, py2 + y1_offset
            plates.append((px1, plate_box.cls, (px1, py1, px2, py2)))
    plates.sort(key=lambda x: x[0])  # Sort plates by x1 coordinate
    return plates

def draw_license_plate_boxes(frame, plates, detected_classes):
    """Draw license plate boxes on the frame and update detected classes."""
    for plate in plates:
        px1, cls, (x1_plate, y1_plate, x2_plate, y2_plate) = plate
        cv2.rectangle(frame, (x1_plate, y1_plate), (x2_plate, y2_plate), (255, 255, 0), 2)  # Blue rectangle for plates
        clsname = plate_model.names[int(cls)]
        detected_classes.append(clsname)

def arrange_detected_classes(detected_classes, drv_lic_thai):
    """Arrange detected classes to prioritize provinces."""
    for item in detected_classes:
        if item in drv_lic_thai.PROVINCE_MAPPING:
            detected_classes.remove(item)
            detected_classes.append(item)
    return detected_classes

def get_thai_license_plate_from_video(video_path: str):
    drv_lic_thai: ThaiLicenseHelper = ThaiLicenseHelper()
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        detected_classes = []
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (1280, 720))
        # Detect vehicles
        vehicle_results = vehicle_model(frame, conf=0.3, verbose=False)
        vehicle_rois = process_vehicle_boxes(vehicle_results, frame)

        # Detect license plates for each vehicle ROI
        for car_roi, x1, y1 in vehicle_rois:
            plate_results = plate_model(car_roi, conf=0.3, verbose=False)
            plates = process_license_plate_boxes(plate_results, x1, y1)
            draw_license_plate_boxes(frame, plates, detected_classes)

        # Arrange and process detected classes
        detected_classes = arrange_detected_classes(detected_classes, drv_lic_thai)
        combined_text = "".join(drv_lic_thai.get_thai_character(newval) for newval in detected_classes)
        license_plate, province = drv_lic_thai.split_license_plate_and_province(combined_text)
        print("Driver license plate:", license_plate, "province:", province)

        # Display the license plate and province on the frame
        cv2.imshow("License Plate Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    video_path = "videos/road_th.mp4"
    get_thai_license_plate_from_video(video_path)

if __name__ == "__main__":
    main()