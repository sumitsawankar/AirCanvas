import cv2
import time
import sys
from src.config import (
    WINDOW_NAME, WIDTH, HEIGHT, COLOR_PALETTE,
    DEFAULT_BRUSH_SIZE, DEFAULT_ERASER_SIZE, TOOLBAR_HEIGHT
)
from src.tracker import HandTracker
from src.canvas import CanvasManager
from src.ui import UIRenderer

def main():
    # 1. Initialize Webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit(1)

    # Set frame dimensions
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # 2. Initialize Core Managers
    tracker = HandTracker(max_hands=1)
    canvas_manager = CanvasManager()
    ui_renderer = UIRenderer()

    # 3. Application State Variables
    active_color = COLOR_PALETTE["RED"]
    active_tool = "draw"  # "draw" or "eraser"
    
    prev_pt = None  # To store the previous finger coordinates for continuous lines
    
    # Hover dwell-time tracking state for action buttons (CLEAR, SAVE)
    hover_button_id = None
    hover_start_time = None
    DWELL_TIME_THRESHOLD = 0.8  # seconds required to hover to trigger actions

    # FPS Calculation
    prev_time = time.time()
    fps_smooth = 30.0

    print("AirCanvas initialized. Press 'q' in the window to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read from webcam.")
            break

        # Mirror frame horizontally for intuitive interaction
        frame = cv2.flip(frame, 1)

        # Process frame for hand landmarks
        results = tracker.process_frame(frame)
        hand_detected = results.multi_hand_landmarks is not None

        # Current pointer state
        gesture = "idle"
        fx, fy = None, None

        if hand_detected:
            # We track the primary hand (first detected)
            hand_landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0]

            # Draw skeleton connections onto feed (for futuristic feedback)
            tracker.draw_landmarks(frame, hand_landmarks)

            # Detect current gesture and get smoothed coordinates of index finger tip
            gesture, (fx, fy) = tracker.get_gesture_and_coords(hand_landmarks, handedness)
        else:
            # If hand is lost, reset coordinates and clear line continuation memory
            tracker.reset_pointer()
            prev_pt = None

        # 4. Action Dwell-Timer and Selection logic
        hovered_btn_id = None
        
        # Merge canvas with frame first (to capture drawings before HUD is drawn)
        merged_frame = canvas_manager.merge(frame)

        if fx is not None and fy is not None:
            # Determine if finger coordinates lie inside the top toolbar area
            if fy < TOOLBAR_HEIGHT:
                # Break drawing connection line when entering toolbar
                prev_pt = None
                
                # Check which button the finger is hovering over
                hovered_btn_id = ui_renderer.draw_hud(
                    merged_frame, (fx, fy), active_color, active_tool, "select", hand_detected, fps_smooth
                )

                if hovered_btn_id:
                    # Resolve button configurations
                    # Find configuration by button ID
                    btn_config = next((b for b in ui_renderer.buttons if b["id"] == hovered_btn_id), None)
                    
                    if btn_config:
                        # Case A: Color selection button (Instant trigger)
                        if btn_config["type"] == "color":
                            active_color = btn_config["color"]
                            active_tool = "draw"
                            hover_button_id = None
                            hover_start_time = None
                        
                        # Case B: Eraser tool button (Instant trigger)
                        elif btn_config["type"] == "eraser":
                            active_tool = "eraser"
                            hover_button_id = None
                            hover_start_time = None
                        
                        # Case C: Action button (Dwell trigger to prevent accidental triggers)
                        elif btn_config["type"] == "action":
                            if hover_button_id != hovered_btn_id:
                                hover_button_id = hovered_btn_id
                                hover_start_time = time.time()
                            else:
                                elapsed = time.time() - hover_start_time
                                # Render progress bar / dwell feedback
                                progress_w = int((elapsed / DWELL_TIME_THRESHOLD) * 100)
                                progress_w = min(progress_w, 100)
                                
                                # Draw a loading progress bar inside the hovered button
                                (x1, y1), (x2, y2) = btn_config["rect"]
                                bar_y = y2 - 5
                                cv2.rectangle(merged_frame, (x1, bar_y), (x1 + int((x2 - x1) * (progress_w / 100)), y2), COLOR_PALETTE["BORDER_GLOW"], -1)

                                if elapsed >= DWELL_TIME_THRESHOLD:
                                    # Trigger the action!
                                    if hovered_btn_id == "CLEAR":
                                        canvas_manager.clear()
                                        ui_renderer.trigger_notification("Canvas Cleared!")
                                    elif hovered_btn_id == "SAVE":
                                        # Save drawing (we save the merged frame showing the drawing overlaid on the camera feed)
                                        success, filename = canvas_manager.save_drawing(canvas_manager.merge(frame))
                                        if success:
                                            ui_renderer.trigger_notification(f"Saved {filename} successfully!")
                                        else:
                                            ui_renderer.trigger_notification(f"Save Failed: {filename}")
                                    
                                    # Reset hover state to prevent immediate re-triggering
                                    hover_button_id = None
                                    hover_start_time = None
                else:
                    hover_button_id = None
                    hover_start_time = None
            else:
                # Reset hover timers when moving out of the toolbar
                hover_button_id = None
                hover_start_time = None

                # 5. Drawing & Erasing state execution (Drawing Area)
                # Apply gesture mode action
                if gesture == "draw":
                    # Drawing mode: draw with current tool (either brush or eraser)
                    if active_tool == "draw":
                        if prev_pt is not None:
                            canvas_manager.draw_line(prev_pt, (fx, fy), active_color, DEFAULT_BRUSH_SIZE)
                        prev_pt = (fx, fy)
                    elif active_tool == "eraser":
                        if prev_pt is not None:
                            canvas_manager.erase_line(prev_pt, (fx, fy), DEFAULT_ERASER_SIZE)
                        prev_pt = (fx, fy)
                        
                elif gesture == "erase":
                    # Open palm gesture activates the eraser automatically
                    if prev_pt is not None:
                        canvas_manager.erase_line(prev_pt, (fx, fy), DEFAULT_ERASER_SIZE)
                    prev_pt = (fx, fy)
                    
                else:
                    # Idle or Select gestures break current drawing stroke
                    prev_pt = None
        else:
            # Reset pointer variables if finger is lost
            prev_pt = None
            hover_button_id = None
            hover_start_time = None

        # 6. Render HUD elements over the merged output
        # If the finger is in the drawing area, we render standard HUD
        if fy is None or fy >= TOOLBAR_HEIGHT:
            ui_renderer.draw_hud(
                merged_frame, (fx or -100, fy or -100), active_color, active_tool, gesture, hand_detected, fps_smooth
            )

        # 7. FPS Calculation & Update
        curr_time = time.time()
        raw_fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time
        # Smooth FPS to avoid rapid flickering
        fps_smooth = fps_smooth * 0.9 + raw_fps * 0.1

        # 8. Display Output Window
        cv2.imshow(WINDOW_NAME, merged_frame)

        # 9. Keyboard Shortcuts
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas_manager.clear()
            ui_renderer.trigger_notification("Canvas Cleared! (Key Shortcut)")
        elif key == ord('s'):
            success, filename = canvas_manager.save_drawing(canvas_manager.merge(frame))
            if success:
                ui_renderer.trigger_notification(f"Saved {filename}! (Key Shortcut)")
            else:
                ui_renderer.trigger_notification(f"Save Failed! (Key Shortcut)")

    # Cleanup resource captures
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

if __name__ == "__main__":
    main()
