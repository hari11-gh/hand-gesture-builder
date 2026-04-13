import cv2
from src.hand_tracker import HandTracker
from src.gesture_detector import GestureDetector
from src.block import Block

cap = cv2.VideoCapture(0)

tracker = HandTracker()
gesture = GestureDetector()

block = Block(200, 200)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, landmarks = tracker.get_hand_landmarks(img)

    if landmarks:
        cursor_x, cursor_y = landmarks[8]

        # draw cursor
        cv2.circle(img, (cursor_x, cursor_y), 10, (0, 255, 0), -1)

        is_dragging = gesture.is_pinching(landmarks)

        block.update(cursor_x, cursor_y, is_dragging)

    block.draw(img)

    cv2.imshow("Gesture Builder", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()