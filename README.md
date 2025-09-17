# MediaPipe Pose Visualizer

## Project Overview
This project demonstrates human pose estimation using [MediaPipe](https://developers.google.com/mediapipe) and [OpenCV](https://opencv.org/).  
It provides two main functionalities:
- **2D Pose Overlay**: Draws skeletal landmarks directly on video frames.  
- **3D Pose Visualization**: Renders a live 3D skeleton using Matplotlib while simultaneously displaying the video feed.  

The goal is to help developers and researchers visualize human movement in both 2D and 3D space for applications such as fitness tracking, motion analysis, and computer vision experiments.

## Setup and Installation

### Prerequisites
- **Python 3.11** required (other versions not supported).  
  Download and install from [Python 3.11](https://www.python.org/downloads/release/python-3110/).  
- pip (Python package manager).  

### Create and Activate Virtual Environment (Windows)
```bash
# Check Python version
py -3.11 --version

# Create virtual environment
py -3.11 -m venv myproject

# Activate it
myproject\Scripts\activate

# Verify versions
python --version
pip --version
```

**Note**: Your prompt should now show `(myproject)`.  
**Warning**: This project only works with Python 3.11.

Once activated, install dependencies:
```bash
pip install -r requirements.txt
```

## Folder Structure
```
mediapipe-pose-visualizer/
│
├── 2d_web_cam.py                # Draws 2D pose landmarks on webcam feed
├── pose_detection_2d.py         # Draws 2D pose landmarks on video frames
├── pose_detection_3d.py         # Visualizes 3D skeleton with Matplotlib
│
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## File Descriptions
- **2d_web_cam.py**  
  - Captures live webcam feed using OpenCV.  
  - Uses MediaPipe Pose to detect body landmarks.  
  - Draws 2D skeleton overlay on each frame.  
  - Displays processed feed in real-time at 960x540 resolution with FPS counter.  

- **pose_detection_2d.py**  
  - Reads a video file using OpenCV.  
  - Uses MediaPipe Pose to detect body landmarks.  
  - Draws 2D skeleton overlay on each video frame.  
  - Displays processed video in real-time at 484x692 resolution.  

- **pose_detection_3d.py**  
  - Reads a video file using OpenCV.  
  - Extracts 3D landmark coordinates (x, y, z) using MediaPipe Pose.  
  - Renders real-time 3D skeleton using Matplotlib with front-view perspective.  
  - Simultaneously displays the original video at 484x692 resolution with FPS counter.  

- **requirements.txt**  
  - Lists dependencies: `opencv-python`, `mediapipe`, `matplotlib`, `numpy`.  

## Approach and Architecture
1. **Input Handling**
   - Load video file or webcam feed with OpenCV.
   - Process frame by frame in a loop.

2. **Pose Detection**
   - Convert each frame from BGR (OpenCV) to RGB (MediaPipe requirement).
   - Run MediaPipe Pose model to detect 33 body landmarks.

3. **Data Extraction**
   - Collect normalized (x, y, z) coordinates for each landmark.
   - Use indices to connect joints (shoulders, elbows, knees, etc.).

4. **Visualization**
   - **2D Mode**: Overlay skeleton on webcam or video frames using OpenCV drawing utilities.  
   - **3D Mode**: Plot landmarks and connections in Matplotlib with real-time updates.  

5. **Output**
   - Real-time display of processed webcam or video feed (2D).  
   - Interactive 3D skeleton visualization (3D).  

## Key Features
- ✅ Real-time human pose estimation from webcam or video.  
- ✅ 2D skeleton overlay on webcam or video frames.  
- ✅ Interactive 3D skeleton visualization with depth information.  
- ✅ Works with webcam or any video file input.  
- ✅ Easy to extend for tracking, motion analysis, or angle measurement.  

## Usage Instructions

### Run 2D Pose Overlay (Webcam)
```bash
python 2d_web_cam.py
```

### Run 2D Pose Overlay (Video)
```bash
python pose_detection_2d.py
```

### Run 3D Pose Visualization
```bash
python pose_detection_3d.py
```

- Replace `video.mp4` in `pose_detection_2d.py` and `pose_detection_3d.py` with your own video file path.  
- Press **ESC** or **q** to exit early.  

## Technical Details
- **Dependencies**:
  - `opencv-python` → Video handling and display  
  - `mediapipe` → Pretrained pose detection model  
  - `matplotlib` → 3D skeleton plotting  
  - `numpy` → Efficient coordinate processing  

- **System Requirements**:
  - Works on Windows, macOS, or Linux.  
  - CPU-based execution (no GPU required, but GPU acceleration possible with MediaPipe).  
  - Real-time performance depends on system specs and video resolution.  

## License
MIT License – free to use and modify.