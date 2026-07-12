import os
import re
import cv2
import numpy as np
from src.config import WIDTH, HEIGHT

class CanvasManager:
    def __init__(self):
        """Initializes a blank black canvas for drawing."""
        self.width = WIDTH
        self.height = HEIGHT
        # 3-channel canvas (0,0,0 is transparent background)
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def draw_line(self, pt1, pt2, color, thickness):
        """Draws a line segment on the canvas."""
        cv2.line(self.canvas, pt1, pt2, color, thickness)

    def erase_line(self, pt1, pt2, thickness):
        """Erases by drawing black pixels (0, 0, 0) on the canvas."""
        cv2.line(self.canvas, pt1, pt2, (0, 0, 0), thickness)

    def clear(self):
        """Resets the canvas to black (empty)."""
        self.canvas.fill(0)

    def merge(self, frame):
        """
        Merges the drawing canvas with the live webcam feed.
        Drawn pixels on the canvas (non-black) replace the camera frame pixels.
        """
        # Convert canvas to grayscale
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        
        # Create a binary mask where drawn pixels are 255 (white) and background is 0
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        
        # Invert the mask: background is 255, drawn area is 0
        mask_inv = cv2.bitwise_not(mask)
        
        # Black out the area of the drawing in the webcam frame
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        # Take only the drawn pixels from the canvas
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        
        # Combine the webcam background and canvas foreground
        merged = cv2.add(frame_bg, canvas_fg)
        return merged

    def save_drawing(self, merged_frame, output_dir="."):
        """
        Saves the merged webcam feed and drawing as a PNG image.
        Filename auto-increments: drawing_001.png, drawing_002.png, etc.
        """
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Look for existing drawing files to determine next index
            files = os.listdir(output_dir)
            pattern = re.compile(r"drawing_(\d+)\.png")
            max_idx = 0
            
            for file in files:
                match = pattern.match(file)
                if match:
                    idx = int(match.group(1))
                    if idx > max_idx:
                        max_idx = idx

            next_idx = max_idx + 1
            filename = f"drawing_{next_idx:03d}.png"
            filepath = os.path.join(output_dir, filename)

            # Save frame
            success = cv2.imwrite(filepath, merged_frame)
            if success:
                return True, filename
            else:
                return False, "Failed to write file"
        except Exception as e:
            return False, str(e)
