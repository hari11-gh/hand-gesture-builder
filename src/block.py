import cv2

class Block:
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.dragging = False

    def draw(self, img):
        cv2.rectangle(
            img,
            (self.x, self.y),
            (self.x + self.size, self.y + self.size),
            (0, 0, 255),
            -1
        )

    def update(self, cursor_x, cursor_y, dragging):
        if dragging:
            if (self.x < cursor_x < self.x + self.size and
                self.y < cursor_y < self.y + self.size):
                self.x = cursor_x - self.size // 2
                self.y = cursor_y - self.size // 2