import cv2
import time
from src.config import (
    WIDTH, HEIGHT, TOOLBAR_HEIGHT, BUTTON_PADDING,
    BUTTONS_CONFIG, COLOR_PALETTE, DEFAULT_BRUSH_SIZE, DEFAULT_ERASER_SIZE
)

def draw_rounded_rect(img, pt1, pt2, color, thickness=-1, radius=10):
    """Draws a rounded rectangle using line, circle, and ellipse drawings."""
    x1, y1 = pt1
    x2, y2 = pt2

    # Prevent radius from exceeding dimensions
    radius = min(radius, abs(x2 - x1) // 2, abs(y2 - y1) // 2)

    if thickness == -1:
        # Draw horizontal and vertical interior rectangles
        cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        # Draw corners
        cv2.circle(img, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(img, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(img, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(img, (x2 - radius, y2 - radius), radius, color, -1)
    else:
        # Draw edges
        cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
        # Draw corner arcs
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)


class UIRenderer:
    def __init__(self):
        """Precomputes button positions for performance."""
        self.buttons = []
        self._calculate_button_positions()
        
        # Toast notifications queue
        self.notification_msg = ""
        self.notification_expiry = 0.0

    def _calculate_button_positions(self):
        """Calculates coordinates for all toolbar buttons dynamically."""
        total_buttons = len(BUTTONS_CONFIG)
        btn_width = (WIDTH - (BUTTON_PADDING * (total_buttons + 1))) // total_buttons
        
        y1 = BUTTON_PADDING
        y2 = TOOLBAR_HEIGHT - BUTTON_PADDING

        for i, config in enumerate(BUTTONS_CONFIG):
            x1 = BUTTON_PADDING + i * (btn_width + BUTTON_PADDING)
            x2 = x1 + btn_width
            
            self.buttons.append({
                "id": config["id"],
                "label": config["label"],
                "color": config["color"],
                "type": config["type"],
                "rect": ((x1, y1), (x2, y2))
            })

    def trigger_notification(self, msg, duration=3.0):
        """Saves a temporary notification message to be drawn on screen."""
        self.notification_msg = msg
        self.notification_expiry = time.time() + duration

    def draw_hud(self, frame, finger_coords, active_color, active_tool, current_mode, hand_detected, fps):
        """Renders the entire dashboard UI overlay onto the frame."""
        # 1. Glassmorphism Toolbar Background (translucent top bar)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (WIDTH, TOOLBAR_HEIGHT), COLOR_PALETTE["HUD_BG"], -1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

        # 2. Render Buttons
        fx, fy = finger_coords
        hovered_button_id = None

        # Check if the finger is inside toolbar area
        if fx is not None and fy is not None:
            for btn in self.buttons:
                (x1, y1), (x2, y2) = btn["rect"]
                if x1 <= fx <= x2 and y1 <= fy <= y2:
                    hovered_button_id = btn["id"]
                    break

        for btn in self.buttons:
            (x1, y1), (x2, y2) = btn["rect"]
            is_hovered = btn["id"] == hovered_button_id
            
            # Determine if button is currently active
            is_active = False
            if btn["type"] == "color" and active_tool == "draw" and btn["color"] == active_color:
                is_active = True
            elif btn["type"] == "eraser" and active_tool == "eraser":
                is_active = True

            # Draw glow border for active or hovered buttons
            if is_active:
                # Active button: solid neon glow border
                draw_rounded_rect(frame, (x1 - 2, y1 - 2), (x2 + 2, y2 + 2), COLOR_PALETTE["BORDER_GLOW"], 3, radius=12)
            elif is_hovered:
                # Hovered button: thinner cyan border
                draw_rounded_rect(frame, (x1 - 2, y1 - 2), (x2 + 2, y2 + 2), COLOR_PALETTE["GRAY"], 2, radius=12)

            # Draw main button fill
            btn_color = btn["color"]
            # If hovered and not color type, make fill slightly lighter
            if is_hovered and btn["type"] != "color":
                btn_color = tuple(min(c + 40, 255) for c in btn["color"])
            
            draw_rounded_rect(frame, (x1, y1), (x2, y2), btn_color, -1, radius=10)

            # Draw labels
            text_color = COLOR_PALETTE["WHITE"]
            # If color button is black or yellow, adjust text color for readability
            if btn["id"] in ["YELLOW", "WHITE", "ERASER"]:
                text_color = COLOR_PALETTE["BG_DARK"]
            
            # Text size calculation for centering
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.55
            thickness = 2
            text_size = cv2.getTextSize(btn["label"], font, font_scale, thickness)[0]
            text_x = x1 + (x2 - x1 - text_size[0]) // 2
            text_y = y1 + (y2 - y1 + text_size[1]) // 2

            # Text shadow for colored buttons if white text
            if text_color == COLOR_PALETTE["WHITE"]:
                cv2.putText(frame, btn["label"], (text_x + 1, text_y + 1), font, font_scale, COLOR_PALETTE["BG_DARK"], thickness)
            
            cv2.putText(frame, btn["label"], (text_x, text_y), font, font_scale, text_color, thickness)

        # 3. Stats Card (Glassmorphism bottom panel)
        card_w, card_h = 280, 110
        card_x, card_y = 15, HEIGHT - card_h - 15
        stats_overlay = frame.copy()
        draw_rounded_rect(stats_overlay, (card_x, card_y), (card_x + card_w, card_y + card_h), COLOR_PALETTE["HUD_BG"], -1, radius=12)
        cv2.addWeighted(stats_overlay, 0.65, frame, 0.35, 0, frame)
        # Stats card border
        draw_rounded_rect(frame, (card_x, card_y), (card_x + card_w, card_y + card_h), COLOR_PALETTE["GRAY"], 1, radius=12)

        # Text on Stats Card
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.45
        text_color = COLOR_PALETTE["WHITE"]
        dy = 22

        # 3a. FPS Text
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(frame, fps_text, (card_x + 15, card_y + 25), font, font_scale, text_color, 1)

        # 3b. Mode Text
        mode_text = f"Mode: {current_mode.upper()}"
        cv2.putText(frame, mode_text, (card_x + 15, card_y + 25 + dy), font, font_scale, text_color, 1)

        # 3c. Active Tool / Color indicator
        tool_desc = "Eraser" if active_tool == "eraser" else "Brush"
        tool_text = f"Active: {tool_desc}"
        cv2.putText(frame, tool_text, (card_x + 15, card_y + 25 + 2 * dy), font, font_scale, text_color, 1)

        # Draw a small preview dot of current color
        if active_tool == "draw":
            cv2.circle(frame, (card_x + 160, card_y + 25 + 2 * dy - 4), 6, active_color, -1)
            cv2.circle(frame, (card_x + 160, card_y + 25 + 2 * dy - 4), 6, COLOR_PALETTE["WHITE"], 1)

        # 3d. Hand Status Circle
        status_text = "Hand Tracker:"
        cv2.putText(frame, status_text, (card_x + 15, card_y + 25 + 3 * dy), font, font_scale, text_color, 1)
        status_color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.circle(frame, (card_x + 140, card_y + 25 + 3 * dy - 4), 6, status_color, -1)

        # 4. Save/Toast Notification rendering
        if time.time() < self.notification_expiry:
            toast_w, toast_h = 420, 50
            toast_x = (WIDTH - toast_w) // 2
            toast_y = HEIGHT - 80
            toast_overlay = frame.copy()
            draw_rounded_rect(toast_overlay, (toast_x, toast_y), (toast_x + toast_w, toast_y + toast_h), COLOR_PALETTE["HUD_BG"], -1, radius=8)
            cv2.addWeighted(toast_overlay, 0.75, frame, 0.25, 0, frame)
            # Glowing border for notification
            draw_rounded_rect(frame, (toast_x, toast_y), (toast_x + toast_w, toast_y + toast_h), COLOR_PALETTE["BORDER_GLOW"], 1, radius=8)

            t_size = cv2.getTextSize(self.notification_msg, font, 0.5, 1)[0]
            tx = toast_x + (toast_w - t_size[0]) // 2
            ty = toast_y + (toast_h + t_size[1]) // 2
            cv2.putText(frame, self.notification_msg, (tx, ty), font, 0.5, COLOR_PALETTE["BORDER_GLOW"], 1, cv2.LINE_AA)

        # 5. Cursor/Reticle Feedback
        if fx is not None and fy is not None:
            # Draw reticle
            if current_mode == "draw":
                # Pulse outline using sine wave on time
                pulse = int(2 * (time.time() % 1))
                cv2.circle(frame, (fx, fy), DEFAULT_BRUSH_SIZE + 2 + pulse, active_color, 1, cv2.LINE_AA)
                cv2.circle(frame, (fx, fy), 2, active_color, -1)
            elif current_mode == "erase":
                # Eraser circle outline
                cv2.circle(frame, (fx, fy), DEFAULT_ERASER_SIZE // 2, COLOR_PALETTE["WHITE"], 1, cv2.LINE_AA)
                cv2.circle(frame, (fx, fy), 2, COLOR_PALETTE["GRAY"], -1)
            elif current_mode == "select":
                # Cursor with crosshair
                cv2.drawMarker(frame, (fx, fy), COLOR_PALETTE["BORDER_GLOW"], cv2.MARKER_CROSS, 20, 1)
            else:
                # Idle: small grey dot
                cv2.circle(frame, (fx, fy), 4, COLOR_PALETTE["GRAY"], 1)

        return hovered_button_id
