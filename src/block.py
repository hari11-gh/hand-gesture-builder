import cv2

class Block:
    def __init__(self, x, y, size=60):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, img):
        overlay = img.copy()

        # ===== 1. HOLOGRAM FILL =====
        cv2.rectangle(
            overlay,
            (self.x, self.y),
            (self.x + self.size, self.y + self.size),
            (255, 255, 0),
            -1
        )

        # transparency blend
        cv2.addWeighted(overlay, 0.18, img, 0.82, 0, img)

        # ===== 2. DEPTH ILLUSION (fake 3D) =====
        offset = 6

        # top face
        cv2.line(img,
                 (self.x, self.y),
                 (self.x + offset, self.y - offset),
                 (255, 255, 0), 1)

        cv2.line(img,
                 (self.x + self.size, self.y),
                 (self.x + self.size + offset, self.y - offset),
                 (255, 255, 0), 1)

        cv2.line(img,
                 (self.x + offset, self.y - offset),
                 (self.x + self.size + offset, self.y - offset),
                 (255, 255, 0), 1)

        # side face
        cv2.line(img,
                 (self.x + self.size, self.y),
                 (self.x + self.size + offset, self.y - offset),
                 (255, 255, 0), 1)

        cv2.line(img,
                 (self.x + self.size, self.y + self.size),
                 (self.x + self.size + offset, self.y + self.size - offset),
                 (255, 255, 0), 1)

        cv2.line(img,
                 (self.x + self.size + offset, self.y - offset),
                 (self.x + self.size + offset, self.y + self.size - offset),
                 (255, 255, 0), 1)

        # ===== 3. GLOW EFFECT =====
        for i in range(8, 0, -2):
            cv2.rectangle(
                img,
                (self.x - i, self.y - i),
                (self.x + self.size + i, self.y + self.size + i),
                (255, 255, 0),
                1
            )

        # ===== 4. MAIN BORDER =====
        cv2.rectangle(
            img,
            (self.x, self.y),
            (self.x + self.size, self.y + self.size),
            (255, 255, 0),
            2
        )

        # ===== 5. TECH GRID (inside) =====
        step = self.size // 3
        for i in range(1, 3):
            # vertical lines
            cv2.line(img,
                     (self.x + i * step, self.y),
                     (self.x + i * step, self.y + self.size),
                     (255, 255, 0), 1)

            # horizontal lines
            cv2.line(img,
                     (self.x, self.y + i * step),
                     (self.x + self.size, self.y + i * step),
                     (255, 255, 0), 1)

        # ===== 6. CORNER NODES =====
        for (px, py) in [
            (self.x, self.y),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]:
            cv2.circle(img, (px, py), 4, (255, 255, 255), -1)