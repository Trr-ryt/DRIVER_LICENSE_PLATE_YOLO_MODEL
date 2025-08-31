from ultralytics import YOLO
import cv2

class YOLOModelHelper:
    @staticmethod
    def transform_to_ncnn_model(pt_model_path: str, ncnn_model_path: str) -> None:
        # Load a YOLOv8 PyTorch model
        model = YOLO(pt_model_path)

        # Export the model to NCNN format
        model.export(format="ncnn")  # creates 'yolo11n_ncnn_model'

        # Load the exported NCNN model
        ncnn_model = YOLO(ncnn_model_path)
        print(ncnn_model)  # Print the model summary
    
    @staticmethod
    def model_predict_obj(video_path: str) -> None:
        # Load a YOLO11n PyTorch model
        model = YOLO("models/yolo11n.pt")

        # Export the model to NCNN format
        model.export(format="ncnn")  # creates 'yolo11n_ncnn_model'

        # Load the exported NCNN model
        ncnn_model = YOLO("models/yolo11n_ncnn_model")
        cap = cv2.VideoCapture(video_path)  # Open the video file
        while cap.isOpened():
            ret, frame = cap.read()  # Read a frame from the video
            if not ret:
                break
            results = ncnn_model(frame, conf=0.2, iou=0.45, verbose=False)
            for val in results:
                frame = val.plot()  # Plot the results on the image
            cv2.imshow("Detection", frame)  # Display the frame with detections
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
                break
        cap.release()  # Release the video capture object
        cv2.destroyAllWindows()  # Close all OpenCV windows