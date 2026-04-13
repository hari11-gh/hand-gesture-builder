import math

class GestureDetector:
    def is_pinching(self, landmarks):
        if len(landmarks) < 9:
            return False

        x1, y1 = landmarks[4]   # thumb tip
        x2, y2 = landmarks[8]   # index tip

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance < 40