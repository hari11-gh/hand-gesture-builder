import math

class GestureDetector:

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def is_pinching(self, landmarks):
        if len(landmarks) < 9:
            return False

        return self.distance(landmarks[4], landmarks[8]) < 40

    def is_open_palm(self, landmarks):
        if len(landmarks) < 21:
            return False

        # fingertips
        tips = [8, 12, 16, 20]

        # check if fingers are extended
        count = 0
        for tip in tips:
            if landmarks[tip][1] < landmarks[tip - 2][1]:
                count += 1

        return count >= 3  # 3+ fingers up

    def is_fist(self, landmarks):
        if len(landmarks) < 21:
            return False

        tips = [8, 12, 16, 20]

        closed = 0
        for tip in tips:
        # finger tip below its joint → folded
            if landmarks[tip][1] > landmarks[tip - 2][1]:
                closed += 1

        return closed >= 3
    
    def is_two_fingers(self, landmarks):
        if len(landmarks) < 21:
            return False

    # index and middle up, others down
        return (
            landmarks[8][1] < landmarks[6][1] and
            landmarks[12][1] < landmarks[10][1] and
            landmarks[16][1] > landmarks[14][1] and
            landmarks[20][1] > landmarks[18][1]
        )