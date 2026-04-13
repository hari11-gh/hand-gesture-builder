import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.tasks.vision.HandLandmarker
        self.base_options = mp.tasks.BaseOptions(model_asset_path="hand_landmarker.task")

        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=self.base_options,
            num_hands=1
        )

        self.detector = self.mp_hands.create_from_options(self.options)

    def get_hand_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        result = self.detector.detect(mp_image)

        landmarks = []

        if result.hand_landmarks:
            h, w, _ = img.shape

            for hand_landmarks in result.hand_landmarks:
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((cx, cy))

        return img, landmarks