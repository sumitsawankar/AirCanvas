# AirCanvas – Gesture-Based Virtual Drawing Application

A sleek, premium virtual drawing desktop application written in Python. Draw in the air using your webcam, track gestures with MediaPipe, and interact with a modern glassmorphism HUD interface rendered in real-time.

---

## Features

- **Sleek HUD Overlay**: Glassmorphism semi-transparent top toolbar and dashboard stats panel.
- **Micro-Interactions**: Hover states, active borders, and dynamic reticle cursors for visual feedback.
- **Accidental Click Prevention (Dwell Selector)**: Actions like **Clear Canvas** and **Save Drawing** require hovering over the button for 0.8 seconds. A visual progress indicator updates during the dwell time.
- **Smooth Coordinates (EMA Filter)**: Coordinates are smoothed via Exponential Moving Average to prevent finger jitter.
- **Automatic Erase Mode**: Raising all fingers (open palm) automatically switches the brush into an Eraser.
- **Smart Saved File Incrementor**: Saves your masterpieces as `drawing_001.png`, `drawing_002.png`, etc., without overwriting past work.

---

## Gesture Guide

| Gesture | Fingers Raised | Mode | Action |
| --- | --- | --- | --- |
| **Draw** | Index Finger Only | Drawing Mode | Draws a continuous stroke on the canvas. |
| **Select / Hover** | Index & Middle Fingers | Hover Mode | Moves the cursor without drawing (for selecting tools). |
| **Erase** | Open Palm (All Fingers Up) | Eraser Mode | Sweeps away strokes with a wide brush. |
| **Idle** | Any other finger combination | Idle | Stop drawing and hover without drawing. |

---

## Keyboard Shortcuts

- `q` : Quit the application.
- `c` : Clear canvas instantly.
- `s` : Save drawing instantly.

---

## Setup & Running

### 1. Requirements

Ensure you have Python 3.11+ installed. Run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```

### 2. Launch the Application

Run the application entry point:

```bash
python app.py
```
