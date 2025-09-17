import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

mp_pose = mp.solutions.pose

# Define body connections
POSE_CONNECTIONS = [
    (11, 13), (13, 15),   # left arm
    (12, 14), (14, 16),   # right arm
    (11, 12),             # shoulders
    (23, 24),             # hips
    (11, 23), (12, 24),   # torso
    (23, 25), (25, 27),   # left leg
    (24, 26), (26, 28),   # right leg
    (27, 29), (29, 31),   # left foot
    (28, 30), (30, 32)    # right foot
]

video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f"Video FPS: {fps}")

# Setup matplotlib 3D plot
plt.ion()
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# Set up proper viewing angles
ax.view_init(elev=75, azim=-105)  # Front view with better perspective

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    frame_count = 0
    last_time = cv2.getTickCount()
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Skip frames to improve performance (process every 2nd frame)
        frame_count += 1
        if frame_count % 2 != 0:  # Process every other frame
            continue

        # Convert BGR -> RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            xs = np.array([lm.x for lm in landmarks])
            ys = np.array([lm.y for lm in landmarks])
            zs = np.array([lm.z for lm in landmarks])

            # Fix coordinate system
            ys = 1 - ys  # Flip Y axis
            zs = -zs     # Flip Z axis

            ax.cla()

            # Plot landmarks
            ax.scatter(xs, ys, zs, c="r", marker="o", s=30)

            # Plot connections
            for c in POSE_CONNECTIONS:
                ax.plot(
                    [xs[c[0]], xs[c[1]]],
                    [ys[c[0]], ys[c[1]]],
                    [zs[c[0]], zs[c[1]]],
                    c="b",
                    linewidth=2
                )

            # Set axis limits
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_zlim(-0.5, 0.5)

            # Update viewing angle
             
            #ax.view_init(elev=-90, azim=85)  # Looking at the person from front
            
            ax.view_init(elev=75, azim=-105)  # Looking at the person from front
            
            # Add grid and labels
            ax.grid(True, alpha=0.3)
            ax.set_xlabel("X (Left/Right)")
            ax.set_ylabel("Y (Up/Down)")
            ax.set_zlabel("Z (Depth - Towards/Away)")
            ax.set_title("3D Pose Skeleton - Front View")

            # Use minimal pause for better speed
            plt.pause(0.0001)  # Reduced from 0.001

        # Show original video in OpenCV
        cv2.imshow("Video", cv2.resize(frame, (484, 692)))

        # Calculate and display FPS
        current_time = cv2.getTickCount()
        fps_calc = 1 / ((current_time - last_time) / cv2.getTickFrequency())
        last_time = current_time
        
        # Display FPS on video
        cv2.putText(frame, f'FPS: {int(fps_calc)}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()