import cv2
import socket
from src.hand_tracker import HandTracker

# UDP setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 5055)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

tracker = HandTracker()

# smoothing
prev_x, prev_y = 0, 0
smoothening = 5

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, landmarks = tracker.get_hand_landmarks(img)

    if landmarks:
        raw_x, raw_y = landmarks[8]

        # smooth cursor
        cursor_x = prev_x + (raw_x - prev_x) // smoothening
        cursor_y = prev_y + (raw_y - prev_y) // smoothening

        prev_x, prev_y = cursor_x, cursor_y

        # send data
        message = f"{cursor_x},{cursor_y}"
        sock.sendto(message.encode(), server_address)

        # debug dot
        cv2.circle(img, (cursor_x, cursor_y), 10, (0, 255, 0), -1)

    cv2.imshow("Tracker Sender", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()