# 🎨 AirCanvas AI – Gesture-Based Virtual Drawing Application

**AirCanvas AI** is a real-time, gesture-controlled virtual drawing application built with **Python, OpenCV, and MediaPipe**. It transforms your webcam into an intelligent drawing interface, allowing you to create digital sketches in the air using only your hand gestures—no mouse, stylus, or touchscreen required.

By leveraging **Computer Vision** and **AI-powered hand tracking**, AirCanvas AI detects your hand movements in real time and converts them into smooth digital strokes on a virtual canvas.

---

## ✨ Features

### 🖐️ Real-Time Hand Tracking

* Detects and tracks hand movements using **MediaPipe Hands**.
* Tracks **21 hand landmarks** for accurate gesture recognition.
* Smooth and responsive interaction through a standard webcam.

### ✏️ Air Drawing

* Draw naturally by moving your **index finger** in the air.
* Real-time rendering with smooth brush strokes.
* Touch-free drawing experience.

### 🎨 Multiple Drawing Colors

Choose from multiple brush colors:

* 🔴 Red
* 🟢 Green
* 🔵 Blue
* 🟡 Yellow

### 🧽 Gesture-Based Eraser

* Switch to **Eraser Mode** using a predefined hand gesture.
* Remove unwanted strokes naturally without changing tools manually.

### 🖥️ Live Virtual Canvas

* Drawings are displayed on a transparent virtual canvas over the live webcam feed.
* Creates the illusion of drawing directly in the air.

### ⚡ Smooth Drawing Experience

* Finger positions are smoothed to minimize jitter.
* Continuous line rendering provides a natural writing experience.

### 💾 Save Drawings

* Save your artwork as an image (`.png`) with a single action.
* Automatically generates sequential filenames without overwriting previous drawings.

### 🧹 Clear Canvas

* Instantly clear the entire drawing canvas and start a new sketch.

---

# 🛠️ Tech Stack

* **Python**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **Computer Vision**
* **Machine Learning (MediaPipe Hand Tracking)**

---

# ✋ Gesture Guide

| Gesture                             | Mode           | Action                     |
| ----------------------------------- | -------------- | -------------------------- |
| ☝️ Index Finger Up                  | Draw Mode      | Draw on the virtual canvas |
| ✌️ Index + Middle Finger            | Selection Mode | Select colors or tools     |
| 🖐️ Open Palm                       | Eraser Mode    | Erase existing drawings    |
| ✊ Hand Not Detected / Other Gesture | Idle           | No drawing                 |

---

# 🎨 Available Tools

* 🔴 Red Brush
* 🟢 Green Brush
* 🔵 Blue Brush
* 🟡 Yellow Brush
* 🧽 Eraser
* 🗑️ Clear Canvas
* 💾 Save Drawing

---

# ⌨️ Keyboard Shortcuts

| Key   | Action                   |
| ----- | ------------------------ |
| **Q** | Quit the application     |
| **C** | Clear the canvas         |
| **S** | Save the current drawing |

---

# 📂 Project Structure

```text
AirCanvas-AI/
│
├── app.py                 # Main application
├── requirements.txt       # Project dependencies
├── assets/                # Icons and UI assets
├── saved_drawings/        # Saved drawings
├── README.md
└── LICENSE
```

---

# 🚀 Installation

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

# ▶️ Run the Application

```bash
python app.py
```

Once the application starts:

1. Allow webcam access.
2. Show your hand to the camera.
3. Raise your **index finger** to start drawing.
4. Select colors by hovering over the toolbar.
5. Use the **open palm gesture** to activate the eraser.
6. Save or clear your drawing when needed.

---

# 📸 How It Works

1. Webcam captures live video.
2. MediaPipe detects the user's hand.
3. The system identifies **21 hand landmarks**.
4. The index finger tip is tracked continuously.
5. Finger movement is converted into drawing strokes.
6. Gestures are recognized to switch between drawing, color selection, and erasing.
7. The virtual canvas is merged with the live webcam feed and displayed in real time.

---

# 🌟 Applications

* 🎓 Smart Classrooms
* 🖥️ Interactive Presentations
* 🎨 Digital Art & Sketching
* 📚 E-learning
* 🤖 Computer Vision Demonstrations
* 🧠 AI & Machine Learning Projects
* 👨‍💻 Human–Computer Interaction (HCI)

---

# 🔮 Future Enhancements

* Multiple brush sizes
* More color options
* Undo & Redo functionality
* Shape recognition (Circle, Rectangle, Triangle)
* Handwriting-to-text conversion
* Voice-controlled commands
* Multi-hand support
* PDF export
* Cloud storage integration
* AI-powered shape correction

---

# 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, improve the project, and submit a pull request. Suggestions, feature requests, and bug reports are always appreciated.

---

# 📄 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it for educational and personal projects.

---

# ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub. It helps others discover the project and supports future development.

---

## 👨‍💻 Author

**Sumit Sawankar**

*Building AI-powered applications with Python, Computer Vision, and Machine Learning.*
