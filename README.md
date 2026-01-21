
# Face Recognition & Attendance Management System 🚀

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![DeepLearning](https://img.shields.io/badge/Deep%20Learning-Face%20Recognition-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20Database-purple)

---

## 📌 Project Overview

This project is a ***Real-time Face Recognition and Attendance System*** built using ***Deep Learning and Computer Vision*** techniques. It uses ***InsightFace (RetinaFace for detection and ArcFace for recognition)*** to accurately identify faces from live camera feeds or uploaded images. Each face is converted into a ***512-dimensional embedding*** and stored in ***Qdrant Vector Database*** for fast and reliable matching. A ***FastAPI backend*** handles user registration, face enrollment, and recognition APIs. ***PostgreSQL*** is used to store user details and attendance logs. The system is designed for real-world use cases like employee attendance and access control.

This project is suitable for:
- Office attendance systems
- Secure access control
- Smart entry/exit monitoring
- AI/ML interview and portfolio projects


## 🎯 What This Project Does

- Detects faces in real time
- Recognizes registered users using face embeddings
- Marks **ENTRY** when a user appears
- Marks **EXIT** when a user leaves
- Prevents duplicate entries using time threshold
- Stores attendance logs in a database
- Provides API access to attendance data


## ⚙️ How the Project Works (Step-by-Step)

### 1️⃣ Video Input
- Webcam or camera feed captures live video
- Frames are continuously processed


---

### 2️⃣ Face Detection
- Faces are detected from each frame using a deep learning model
- Bounding boxes are generated for each face


---

### 3️⃣ Face Recognition
- Face embeddings are generated for detected faces
- Embeddings are compared with stored vectors in **Qdrant**
- Best match determines user identity


---

### 4️⃣ Attendance Logic
- If a recognized face appears:
  - ENTRY event is recorded
- If the same face disappears:
  - EXIT event is recorded
- A minimum time gap prevents duplicate logs


---

### 5️⃣ Backend (FastAPI + PostgreSQL)
- FastAPI handles attendance events
- PostgreSQL stores:
  - User details
  - Entry time
  - Exit time


---

### 6️⃣ API Access
- Attendance data can be accessed via REST APIs
- Suitable for dashboards or integration with other systems

---

## 🏗️ System Architecture

Camera → Face Detection → Face Recognition  
→ Attendance Logic → FastAPI  
→ PostgreSQL + Qdrant → API / Dashboard

---

## 🚀 How to Run the Project

### ✅ Requirements
- Python 3.9+
- Webcam / Camera
- PostgreSQL
- Qdrant Vector Database
- Ubuntu / Linux (recommended)


## 1️⃣ Install Dependencies

pip install -r requirements.txt

## 2️⃣ Start Database Services

Start PostgreSQL

Start Qdrant

## 3️⃣ Register Face Data

Capture face images

Generate and store face embeddings in Qdrant

## 4️⃣ Run the Application

uvicorn main.fastapi_app:app --host 0.0.0.0 --port 8000

## ✨ Features

Real-time face detection

Accurate face recognition using embeddings

Automatic ENTRY and EXIT tracking

Duplicate entry prevention

FastAPI-based backend

PostgreSQL attendance database

Qdrant vector search for fast recognition

