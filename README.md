# Face Recognition & Attendance Management System

A real-time **Face Recognition and Attendance Management System** built using **Python**, **Computer Vision**, and **Deep Learning**.  
The system detects faces, recognizes registered users, and automatically records their **entry and exit time**.

This project is created for **learning, practice, and interview demonstration**.

---

## Project Overview

This application captures live video from a camera and performs:

- Face detection in real time
- Face recognition using deep learning
- Automatic attendance marking (ENTRY / EXIT)
- Secure storage of attendance data in a database

---

## How the System Works

1. Camera captures live video frames  
2. Faces are detected from each frame  
3. Face embeddings are generated  
4. Embeddings are matched with stored users  
5. Entry or exit time is saved in the database  

---

## Technologies Used

- Python  
- OpenCV  
- Deep Learning (Face Detection & Recognition)  
- FastAPI  
- PostgreSQL  
- Qdrant (Vector Database)

---

## Project Structure

Face-recog-project/
│
├── main/
│ ├── config.py # Configuration settings
│ ├── db.py # Database connection & queries
│ ├── detection_cli.py # CLI-based face detection
│ ├── face_engine.py # Face detection & recognition logic
│ └── fastapi_app.py # FastAPI application
│
├── run_main.py # Application entry point
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .gitignore # Ignored files



## Installation & Setup

Step 1: Clone the Repository

git clone https://github.com/Mdfaizan8431/face-recognition-detection.git
cd face-recognition-detection

Step 2: Create Virtual Environment

python3 -m venv face_env
source face_env/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Run the Application

python run_main.py

Make sure:

.Camera is connected

.Database is running

.Face data is already registered


Features

Real-time face detection

Accurate face recognition

Automatic attendance logging

Entry and exit tracking

Clean and modular code structure

Important Notes

Do not upload the following files to GitHub:

Videos

Face images

Model weights

Environment files (.env)

These files are excluded using .gitignore.

Use Cases

Office attendance system

Secure access control

Employee monitoring system

AI-based authentication

Why This Project?

Demonstrates real-world AI application

Combines Computer Vision, Backend, and Database

Suitable for interviews and portfolio

Shows good Git and project structure