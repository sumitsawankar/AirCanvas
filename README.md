# AirCanvas AI – Gesture-Based Virtual Drawing Application

**AirCanvas AI** is a real-time gesture-controlled virtual drawing application built using **Python, OpenCV, and MediaPipe**. It enables users to draw on a virtual canvas by moving their hand in front of a webcam, eliminating the need for a mouse, stylus, or touchscreen.

The application uses Computer Vision and AI-powered hand tracking to detect hand movements in real time and convert them into smooth digital drawings.

---

# Features

## Real-Time Hand Tracking

* Detects and tracks hand movements using MediaPipe Hands.
* Tracks 21 hand landmarks for accurate gesture recognition.
* Works in real time using a standard webcam.

## Air Drawing

* Draw by moving your index finger in the air.
* Smooth and responsive brush strokes.
* Touch-free drawing experience.

## Multiple Drawing Colors

Available brush colors include:

* Red
* Green
* Blue
* Yellow

## Gesture-Based Eraser

* Activate eraser mode using a predefined hand gesture.
* Remove unwanted drawings naturally without switching tools manually.

## Live Virtual Canvas

* Drawings are rendered on a transparent virtual canvas over the live webcam feed.
* Creates the effect of drawing directly in the air.

## Smooth Drawing Experience

* Finger coordinates are smoothed to reduce jitter.
* Continuous line rendering provides natural handwriting and drawing.

## Save Drawings

* Save drawings as PNG images.
* Automatically generates sequential filenames without overwriting existing files.

## Clear Canvas

* Instantly clear the entire drawing canvas and begin a new drawing.

---

# Technology Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* Computer Vision
* Machine Learning (MediaPipe Hand Tracking)

---

# Gesture Guide

| Gesture               | Mode           | Action                     |
| --------------------- | -------------- | -------------------------- |
| Index Finger Up       | Draw Mode      | Draw on the virtual canvas |
| Index + Middle Finger | Selection Mode | Select colors or tools     |
| Open Palm             | Eraser Mode    | Erase existing drawings    |
| Other Gestures        | Idle           | No drawing                 |

---

# Available Tools

* Red Brush
* Green Brush
* Blue Brush
* Yellow Brush
* Eraser
* Clear Canvas
* Save Drawing

---

# Keyboard Shortcuts

| Key | Action                   |
| --- | ------------------------ |
| Q   | Quit the application     |
| C   | Clear the canvas         |
| S   | Save the current drawing |

---

# Project Structure

```text
AirCanvas-AI/
│
├── app.py
├── requirements.txt
├── assets/
├── saved_drawings/
├── README.md
└── LICENSE
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AirCanvas-AI.git
```

```bash
cd AirCanvas-AI
```

---

## 2. Create a Virtual Environment (Optional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

```bash
python app.py
```

After launching the application:

1. Allow webcam access.
2. Show your hand to the camera.
3. Raise your index finger to start drawing.
4. Select colors by hovering over the toolbar.
5. Use the open palm gesture to activate the eraser.
6. Save or clear your drawing when needed.

---

# How It Works

1. The webcam captures live video.
2. MediaPipe detects the user's hand.
3. The system identifies 21 hand landmarks.
4. The index finger tip is tracked continuously.
5. Finger movement is converted into drawing strokes.
6. Gestures are recognized for drawing, color selection, and erasing.
7. The virtual canvas is merged with the live webcam feed and displayed in real time.

---

# Applications

* Smart Classrooms
* Interactive Presentations
* Digital Art and Sketching
* E-learning
* Computer Vision Demonstrations
* AI and Machine Learning Projects
* Human–Computer Interaction (HCI)

---

# Future Enhancements

* Multiple brush sizes
* More color options
* Undo and Redo functionality
* Shape recognition
* Handwriting-to-text conversion
* Voice commands
* Multi-hand support
* PDF export
* Cloud storage integration
* AI-powered shape correction

---

# Contributing

Contributions are welcome. Feel free to fork the repository, improve the project, and submit a pull request. Feature requests, bug reports, and suggestions are always appreciated.

---

# License

This project is licensed under the **MIT License**.

---

# Author

**Sumit Sawankar**

Building AI-powered applications using Python, Computer Vision, and Machine Learning.
