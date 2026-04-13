import cv2

class Block:
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.dragging = False

    def draw(self, img):
        # Glow border (futuristic vibe)
        cv2.rectangle(
            img,
            (self.x - 5, self.y - 5),
            (self.x + self.size + 5, self.y + self.size + 5),
            (255, 0, 255),
            1
        )

        # Main face
        cv2.rectangle(
            img,
            (self.x, self.y),
            (self.x + self.size, self.y + self.size),
            (255, 0, 100),
            -1
        )

        # Top highlight
        cv2.line(
            img,
            (self.x, self.y),
            (self.x + self.size, self.y),
            (255, 255, 255),
            2
        )

        # Left highlight
        cv2.line(
            img,
            (self.x, self.y),
            (self.x, self.y + self.size),
            (255, 255, 255),
            2
        )

        # Bottom shadow
        cv2.line(
            img,
            (self.x, self.y + self.size),
            (self.x + self.size, self.y + self.size),
            (50, 0, 50),
            2
        )

        # Right shadow
        cv2.line(
            img,
            (self.x + self.size, self.y),
            (self.x + self.size, self.y + self.size),
            (50, 0, 50),
            2
        )

    def update(self, cursor_x, cursor_y, dragging):
        if dragging:
            if (self.x < cursor_x < self.x + self.size and
                self.y < cursor_y < self.y + self.size):
                self.x = cursor_x - self.size // 2
                self.y = cursor_y - self.size // 2