import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.tasks.vision.HandLandmarker

        self.base_options = mp.tasks.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=self.base_options,
            num_hands=1
        )

        self.detector = self.mp_hands.create_from_options(self.options)

        # 🔥 Manual hand connections (since mp.solutions not available)
        self.connections = [
            (0,1),(1,2),(2,3),(3,4),
            (0,5),(5,6),(6,7),(7,8),
            (5,9),(9,10),(10,11),(11,12),
            (9,13),(13,14),(14,15),(15,16),
            (13,17),(17,18),(18,19),(19,20),
            (0,17)
        ]

    def get_hand_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=img_rgb
        )

        result = self.detector.detect(mp_image)

        landmarks = []

        if result.hand_landmarks:
            h, w, _ = img.shape

            for hand_landmarks in result.hand_landmarks:

                # convert to pixel coords
                for lm in hand_landmarks:
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    landmarks.append((cx, cy))

                # ===== 🦴 DRAW SKELETON =====
                for (start_idx, end_idx) in self.connections:
                    if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):

                        x1 = int(hand_landmarks[start_idx].x * w)
                        y1 = int(hand_landmarks[start_idx].y * h)
                        x2 = int(hand_landmarks[end_idx].x * w)
                        y2 = int(hand_landmarks[end_idx].y * h)

                        # glow effect
                        for i in range(3, 0, -1):
                            cv2.line(img, (x1, y1), (x2, y2), (255, 200, 0), i)

                # ===== ✨ DRAW JOINTS =====
                for lm in hand_landmarks:
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    cv2.circle(img, (cx, cy), 6, (255, 200, 0), 1)
                    cv2.circle(img, (cx, cy), 2, (255, 200, 0), -1)

        return img, landmarks