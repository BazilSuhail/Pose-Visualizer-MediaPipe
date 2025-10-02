import cv2
import mediapipe as mp
import os

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Replace with your image file path
image_path = "Pose-Visualizer-MediaPipe/football.jpeg"  # Use any image file

image = cv2.imread(image_path)

if image is None:
    print("Error: Could not read image file")
    exit()

height, width, _ = image.shape

# Optimize Pose configuration
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    smooth_landmarks=True,
)

# Process the image (convert BGR to RGB)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
rgb_image.flags.writeable = False
results = pose.process(rgb_image)
rgb_image.flags.writeable = True

# Draw landmarks if detected
if results.pose_landmarks:
    landmark_drawing_spec = mp_drawing.DrawingSpec(
        color=(0, 255, 0), thickness=2, circle_radius=3
    )  # Green dots
    connection_drawing_spec = mp_drawing.DrawingSpec(
        color=(0, 0, 255), thickness=2
    )  # Red lines

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=landmark_drawing_spec,
        connection_drawing_spec=connection_drawing_spec,
    )

    # Generate output filename from input
    base_name = os.path.splitext(os.path.basename(image_path))[0]  # e.g., 'babar'
    output_filename = f"{base_name}_output_pose.jpg"
    cv2.imwrite(output_filename, image)
    print(f"Output image saved as '{output_filename}'")

# Resize image for display
DISPLAY_WIDTH, DISPLAY_HEIGHT = 484, 692
display_image = cv2.resize(
    image, (DISPLAY_WIDTH, DISPLAY_HEIGHT), interpolation=cv2.INTER_AREA
)

# Show the image
cv2.imshow("Pose Tracking (Image)", display_image)
cv2.waitKey(0)

# Clean up
pose.close()
cv2.destroyAllWindows()
