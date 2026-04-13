import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils

    def get_hand_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        landmarks = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = img.shape

                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((cx, cy))

                self.mp_draw.draw_landmarks(
                    img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return img, landmarks