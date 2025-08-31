# DRIVER_LICENSE_PLATE_YOLOV11

This project focuses on real-time object detection for vehicles and Thai license plates using the YOLO model accelerated by an NVIDIA GPU, with additional support for Thai character and province recognition, as illustrated in the figure below. The model was implemented on a Raspberry Pi 5; however, performance was not smooth due to reliance on CPU-only processing. For better Perfromance. To improve performance, an AI accelerator (HAT) is required.
![yolo11](https://github.com/user-attachments/assets/e5fff002-96e4-4f3c-a504-eabcd6d14e00)

## Features

- Real-time detection of vehicles and Thai license plates in video streams
- Accurate recognition of Thai license plate characters and provinces
- Pytorch framework to use NVIDIA GPU Processing
- The dataset from Roboflow was trained using YOLOv11 models for robust object detection.
- Modular, extensible codebase with helper modules for vehicles, plates, and license logic
- Interactive video display and annotation using OpenCV

## Requirements

- [Anaconda.org](https://www.anaconda.com/download)
- Python 3.8+
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) (`ultralytics==8.3.3`)
- OpenCV (`opencv-python`)
- Pytorch

##  Install dependencies

Create environment with conda
```bash
conda create --name yolo11 python=3.10
conda activate yolov11
```

Install the ultralytics package using conda
```bash
conda install -c conda-forge ultralytics=8.3.3
```

Install all packages together using conda
```bash
conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=12.1 ultralytics=8.3.3
```

Install related packages
```bash
pip install opencv-contrib-python
pip install shapely
```

## Usage

1. Place your video file in the `videos/` directory (default: `road_th.mp4`).
2. Place YOLO model files in the `models/` directory.
3. Run the main script:
   ```bash
   python main.py
   ```
4. The script will display a window with detected vehicles and license plates, and print recognized license plate and province information.

## Main Components

- `main.py`: Entry point. Loads models, processes video, and displays results.
- `common/`: Helper modules for detection and recognition logic.
  - `drv_lic_helper.py`: Thai character and province mapping utilities.
  - `vehicle_model_helper.py`: Vehicle and plate detection logic.
  - `plate_model_helper.py`: License plate detection and threading.
  - `model_helper.py`: Model conversion and prediction helpers.
- `models`: Model based on YOLOv11
- `videos`: Video sample for testing the model

## Notes

- If you see an error like `moov atom not found`, your video file is likely corrupted or incomplete. Try re-downloading or re-encoding the file.
- Press `q` to exit the video display window.
