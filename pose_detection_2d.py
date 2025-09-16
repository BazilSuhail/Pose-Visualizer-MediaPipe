import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Replace with your video file path
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break  # end of video

        # Convert BGR (OpenCV) -> RGB (MediaPipe expects RGB)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        # Draw landmarks if detected
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        # Resize frame for display (e.g., 800x450)
        display_frame = cv2.resize(frame, (800, 450))

        # Show the smaller frame
        cv2.imshow("Pose Tracking (Video)", display_frame)

        # Press ESC to quit early
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
