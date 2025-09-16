import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

mp_pose = mp.solutions.pose

# Define body connections (same as MediaPipe's POSE_CONNECTIONS)
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

# Open video file
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Setup matplotlib 3D plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

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
            break

        # Convert BGR -> RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Collect x, y, z for all 33 landmarks
            xs = np.array([lm.x for lm in landmarks])
            ys = np.array([lm.y for lm in landmarks])
            zs = np.array([lm.z for lm in landmarks])

            # Clear previous plot
            ax.cla()

            # Plot landmarks
            ax.scatter(xs, ys, zs, c="r", marker="o")

            # Plot connections
            for c in POSE_CONNECTIONS:
                ax.plot(
                    [xs[c[0]], xs[c[1]]],
                    [ys[c[0]], ys[c[1]]],
                    [zs[c[0]], zs[c[1]]],
                    c="b"
                )

            # Set axis limits & labels
            ax.set_xlim(0, 1)
            ax.set_ylim(1, 0)  # flip y-axis to match image space
            ax.set_zlim(-0.5, 0.5)  # relative depth
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z (depth)")
            ax.set_title("3D Pose Skeleton")

            plt.pause(0.001)

        # Show original video in OpenCV
        cv2.imshow("Video", cv2.resize(frame, (640, 360)))

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()
