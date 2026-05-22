import cv2
import numpy as np
import time
import math

# Load Haarcascade
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

# Webcam
cap = cv2.VideoCapture(0)

# Window Size
width = 1280
height = 720

cap.set(3, width)
cap.set(4, height)

score = 0
start_time = time.time()

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
CYAN = (255, 255, 0)
YELLOW = (0, 255, 255)

# Radar animation
radar_angle = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )

    # Futuristic Overlay
    overlay = frame.copy()

    # Transparent dark layer
    cv2.rectangle(overlay, (0, 0), (width, height), (20, 20, 20), -1)
    alpha = 0.2
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # Center Target Area
    center_x = width // 2
    center_y = height // 2

    cv2.circle(frame, (center_x, center_y), 80, CYAN, 2)
    cv2.line(frame, (center_x - 100, center_y),
             (center_x + 100, center_y), CYAN, 2)
    cv2.line(frame, (center_x, center_y - 100),
             (center_x, center_y + 100), CYAN, 2)

    # Radar Animation
    radar_radius = 60
    radar_x = 1100
    radar_y = 120

    cv2.circle(frame, (radar_x, radar_y), radar_radius, GREEN, 2)

    end_x = int(radar_x + radar_radius *
                math.cos(math.radians(radar_angle)))
    end_y = int(radar_y + radar_radius *
                math.sin(math.radians(radar_angle)))

    cv2.line(frame, (radar_x, radar_y), (end_x, end_y), GREEN, 2)

    radar_angle += 5

    # Face Detection
    for (x, y, w, h) in faces:

        cx = x + w // 2
        cy = y + h // 2

        # Face box
        cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 3)

        # Crosshair
        cv2.line(frame, (cx - 30, cy), (cx + 30, cy), RED, 2)
        cv2.line(frame, (cx, cy - 30), (cx, cy + 30), RED, 2)

        # Distance from center
        dist = math.sqrt((cx - center_x) ** 2 +
                         (cy - center_y) ** 2)

        # LOCK SYSTEM
        if dist < 80:

            cv2.putText(frame,
                        "TARGET LOCKED",
                        (x, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        RED,
                        3)

            score += 1

        else:

            cv2.putText(frame,
                        "TRACKING...",
                        (x, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        YELLOW,
                        2)

    # Dashboard
    elapsed = int(time.time() - start_time)

    cv2.rectangle(frame, (20, 20), (350, 180), (0, 0, 0), -1)

    cv2.putText(frame,
                "AI DEFENSE TRACKER",
                (40, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                GREEN,
                3)

    cv2.putText(frame,
                f"SCORE : {score}",
                (40, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                CYAN,
                2)

    cv2.putText(frame,
                f"TIME : {elapsed}s",
                (40, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                CYAN,
                2)

    cv2.putText(frame,
                f"TARGETS : {len(faces)}",
                (40, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                CYAN,
                2)

    # FPS
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    cv2.putText(frame,
                f"FPS : {fps}",
                (1050, 680),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                GREEN,
                2)

    # Decorative Corners
    cv2.rectangle(frame, (5, 5), (width - 5, height - 5), GREEN, 2)

    # Exit Button
    cv2.putText(frame,
                "Press Q to Exit",
                (20, 700),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                RED,
                2)

    cv2.imshow("AI DEFENSE TRACKER", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()