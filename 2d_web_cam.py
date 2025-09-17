import cv2
import mediapipe as mp

# Initialize MediaPipe (outside the loop for better performance)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Open webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Set camera resolution (optional - camera will use its native resolution if not supported)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Higher resolution for better quality
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)             # Set FPS if supported

# Optimize Pose configuration for real-time performance
pose = mp_pose.Pose(
    static_image_mode=False,      # False for video (uses previous frames for tracking)
    model_complexity=1,           # 1=full model (good balance of speed/accuracy)
    enable_segmentation=False,    # Set to False for better performance
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    smooth_landmarks=True         # Enable landmark smoothing
)

# Target display dimensions
TARGET_WIDTH, TARGET_HEIGHT = 960, 540

print("Starting real-time pose tracking...")
print("Press 'ESC' or 'q' to quit")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Error: Failed to read frame from camera")
        break

    # Optional: Resize input frame for faster processing (if camera resolution is very high)
    # frame = cv2.resize(frame, (960, 540))
    
    # Process frame (convert BGR to RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # To improve performance, set image as not writeable
    rgb_frame.flags.writeable = False
    results = pose.process(rgb_frame)
    rgb_frame.flags.writeable = True

    # Draw landmarks if detected
    if results.pose_landmarks:
        # Efficient drawing with custom styling
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )

    # Resize frame for display to exactly 960x540
    display_frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT), interpolation=cv2.INTER_LINEAR)

    # Add FPS counter (optional)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cv2.putText(display_frame, f'FPS: {fps}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Real-time Pose Tracking (960x540)", display_frame)

    # Press ESC or 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):  # ESC or 'q'
        break

# Clean up resources
pose.close()
cap.release()
cv2.destroyAllWindows()

print("Pose tracking stopped. Resources cleaned up.")