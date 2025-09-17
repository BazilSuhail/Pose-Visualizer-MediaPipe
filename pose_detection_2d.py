import cv2
import mediapipe as mp

# Initialized MediaPipe once (outside the loop for better performance)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Replace with your video file path
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

# Get video properties for better processing
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Optimize Pose configuration
pose = mp_pose.Pose(
    static_image_mode=False,  # False for video (uses previous frames for tracking)
    model_complexity=1,       # 0=light, 1=full, 2=heavy
    enable_segmentation=False, # Set to False if you don't need segmentation
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    smooth_landmarks=True     # Enable landmark smoothing
)

# Pre-define display dimensions
DISPLAY_WIDTH, DISPLAY_HEIGHT = 484, 692

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("End of video or error reading frame")
        break

    # Process frame (convert BGR to RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # To improve performance, set image as not writeable
    rgb_frame.flags.writeable = False
    results = pose.process(rgb_frame)
    rgb_frame.flags.writeable = True

    # Draw landmarks if detected
    if results.pose_landmarks:
        # More efficient drawing with custom styling
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )

    # Resize frame for display (using INTER_AREA for better quality when shrinking)
    display_frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT), interpolation=cv2.INTER_AREA)

    # Show frame
    cv2.imshow("Pose Tracking (Video)", display_frame)

    # Press ESC or 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):  # ESC or 'q'
        break

# Clean up
pose.close()  # Explicitly close MediaPipe
cap.release()
cv2.destroyAllWindows()