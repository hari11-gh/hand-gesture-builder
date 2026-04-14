import cv2
from src.hand_tracker import HandTracker
from src.gesture_detector import GestureDetector
from src.block import Block

# 🪟 resizable window
cv2.namedWindow("Hologram Builder", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hologram Builder", 1000, 700)

# 🎥 camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

tracker = HandTracker()
gesture = GestureDetector()

blocks = []
selected_block = None

prev_x, prev_y = 0, 0
smoothening = 5

prev_gesture = "none"

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)

    img, landmarks = tracker.get_hand_landmarks(img)

    current_gesture = "none"

    if landmarks:
        raw_x, raw_y = landmarks[8]

        # 🎯 smoothing
        cursor_x = prev_x + (raw_x - prev_x) // smoothening
        cursor_y = prev_y + (raw_y - prev_y) // smoothening

        prev_x, prev_y = cursor_x, cursor_y

        # ✨ cursor
        cv2.circle(img, (cursor_x, cursor_y), 10, (255, 255, 0), 2)
        cv2.circle(img, (cursor_x, cursor_y), 3, (255, 255, 255), -1)

        # 🧠 gestures
        if gesture.is_pinching(landmarks):
            current_gesture = "pinch"
        elif gesture.is_fist(landmarks):
            current_gesture = "fist"
        elif gesture.is_two_fingers(landmarks):
            current_gesture = "delete"
        elif gesture.is_open_palm(landmarks):
            current_gesture = "open"

        # -------- LOGIC -------- #

        # 🧱 CREATE
        if current_gesture == "fist" and prev_gesture != "fist":
            blocks.append(Block(cursor_x, cursor_y))

        # 🧲 MOVE
        if current_gesture == "pinch":
            if selected_block is None:
                for block in blocks:
                    if (block.x < cursor_x < block.x + block.size and
                        block.y < cursor_y < block.y + block.size):
                        selected_block = block
                        break

            if selected_block:
                selected_block.x = cursor_x - selected_block.size // 2
                selected_block.y = cursor_y - selected_block.size // 2

        # 🗑️ DELETE
        if current_gesture == "delete" and prev_gesture != "delete":
            for block in blocks:
                if (block.x < cursor_x < block.x + block.size and
                    block.y < cursor_y < block.y + block.size):
                    blocks.remove(block)
                    break

        # ✋ RELEASE
        if current_gesture == "open":
            selected_block = None

        prev_gesture = current_gesture

    # 🧊 draw blocks
    for block in blocks:
        block.draw(img)

    # 🧠 UI
    cv2.putText(img, f"Gesture: {prev_gesture}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.putText(img, f"Blocks: {len(blocks)}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("Hologram Builder", img)

    # ⌨️ exit only via keyboard
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()