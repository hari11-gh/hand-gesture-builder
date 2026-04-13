import cv2
from src.hand_tracker import HandTracker
from src.gesture_detector import GestureDetector
from src.block import Block

# Start camera
cap = cv2.VideoCapture(0)

# 🔥 Reduce resolution for speed
cap.set(3, 640)
cap.set(4, 480)

tracker = HandTracker()
gesture = GestureDetector()

block = Block(200, 200)

# 🔥 Smoothing variables
prev_x, prev_y = 0, 0
smoothening = 5  # lower = faster, higher = smoother

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, landmarks = tracker.get_hand_landmarks(img)

    if landmarks:
        raw_x, raw_y = landmarks[8]

        # 🔥 Apply smoothing
        cursor_x = prev_x + (raw_x - prev_x) // smoothening
        cursor_y = prev_y + (raw_y - prev_y) // smoothening

        prev_x, prev_y = cursor_x, cursor_y

        # Draw cursor
        cv2.circle(img, (cursor_x, cursor_y), 10, (0, 255, 0), -1)

        # Detect pinch
        is_dragging = gesture.is_pinching(landmarks)

        # Update block
        block.update(cursor_x, cursor_y, is_dragging)

    # Draw block
    block.draw(img)

    cv2.imshow("Gesture Builder", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()