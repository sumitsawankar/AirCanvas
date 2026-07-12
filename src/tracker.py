import cv2
import mediapipe as mp
import numpy as np
from src.config import SMOOTHING_FACTOR, WIDTH, HEIGHT

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        """Initializes the MediaPipe hands model wrapper."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_styles = mp.solutions.drawing_styles
        
        # Smoothed pointer tracking state
        self.prev_x, self.prev_y = None, None
        
        # Landmark drawing styles (customized for sleek look)
        self.landmark_style = self.mp_draw.DrawingSpec(
            color=(0, 255, 255), thickness=1, circle_radius=3
        )  # Glowing cyan dots
        self.connection_style = self.mp_draw.DrawingSpec(
            color=(240, 240, 240), thickness=2
        )  # Subdued white connections

    def process_frame(self, frame):
        """
        Processes a BGR frame, runs MediaPipe detection, and returns the result.
        The frame is expected to be already mirrored.
        """
        # Convert BGR frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results

    def draw_landmarks(self, frame, hand_landmarks):
        """Draws hand landmarks and connections onto the frame."""
        self.mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            landmark_drawing_spec=self.landmark_style,
            connection_drawing_spec=self.connection_style
        )

    def get_landmarks_list(self, hand_landmarks):
        """Extracts pixel coordinates of all 21 hand landmarks."""
        landmarks = []
        for lm in hand_landmarks.landmark:
            # Map normalized coordinate ratios to frame pixels
            cx, cy = int(lm.x * WIDTH), int(lm.y * HEIGHT)
            landmarks.append((cx, cy))
        return landmarks

    def get_finger_states(self, landmarks, handedness):
        """
        Determines which fingers are raised.
        Returns a dictionary mapping: 'thumb', 'index', 'middle', 'ring', 'pinky' -> bool
        """
        # Landmark index offsets:
        # Index (8: Tip, 6: PIP), Middle (12: Tip, 10: PIP), Ring (16: Tip, 14: PIP), Pinky (20: Tip, 18: PIP)
        fingers = {
            "index": landmarks[8][1] < landmarks[6][1],
            "middle": landmarks[12][1] < landmarks[10][1],
            "ring": landmarks[16][1] < landmarks[14][1],
            "pinky": landmarks[20][1] < landmarks[18][1],
        }

        # Thumb detection (depends on handedness)
        # MediaPipe classification labels are opposite because of mirror/camera mapping,
        # but since we process the already-mirrored frame:
        # Check if hand is Left or Right in coordinates space
        # Left hand thumb tip is to the right of joint 2; Right hand thumb tip is to the left.
        is_left_hand = handedness.classification[0].label == "Left"
        
        # A simple relative horizontal distance check
        if is_left_hand:
            # For a left hand, thumb tip (4) is to the right of IP joint (3) or thumb base (2)
            fingers["thumb"] = landmarks[4][0] > landmarks[2][0]
        else:
            # For a right hand, thumb tip (4) is to the left of IP joint (3) or thumb base (2)
            fingers["thumb"] = landmarks[4][0] < landmarks[2][0]

        return fingers

    def get_gesture_and_coords(self, hand_landmarks, handedness):
        """
        Classifies the current gesture and extracts smoothed index finger tip coordinates.
        Returns:
            gesture_type: str ("draw", "erase", "select", "idle")
            coords: tuple (x, y) or (None, None)
        """
        landmarks = self.get_landmarks_list(hand_landmarks)
        if not landmarks:
            self.reset_pointer()
            return "idle", (None, None)

        finger_states = self.get_finger_states(landmarks, handedness)
        
        # Raw index finger tip coordinates (Landmark 8)
        raw_x, raw_y = landmarks[8]

        # Apply smoothing (EMA filter)
        if self.prev_x is None or self.prev_y is None:
            self.prev_x, self.prev_y = raw_x, raw_y
        else:
            self.prev_x = int(raw_x * (1 - SMOOTHING_FACTOR) + self.prev_x * SMOOTHING_FACTOR)
            self.prev_y = int(raw_y * (1 - SMOOTHING_FACTOR) + self.prev_y * SMOOTHING_FACTOR)

        smoothed_coords = (self.prev_x, self.prev_y)

        # Gesture Classification
        # 1. Eraser Mode: Open Palm (All or at least index, middle, ring, pinky raised)
        if finger_states["index"] and finger_states["middle"] and finger_states["ring"] and finger_states["pinky"]:
            return "erase", smoothed_coords

        # 2. Select / Hover Mode: Index and Middle fingers raised together
        elif finger_states["index"] and finger_states["middle"] and not finger_states["ring"] and not finger_states["pinky"]:
            return "select", smoothed_coords

        # 3. Draw Mode: Only the index finger is raised
        elif finger_states["index"] and not finger_states["middle"] and not finger_states["ring"] and not finger_states["pinky"]:
            return "draw", smoothed_coords

        # 4. Idle Mode
        else:
            # Reset smoothing memory when entering idle to prevent line snapping later
            self.reset_pointer()
            return "idle", smoothed_coords

    def reset_pointer(self):
        """Resets the smoothed coordinate tracker history."""
        self.prev_x, self.prev_y = None, None
