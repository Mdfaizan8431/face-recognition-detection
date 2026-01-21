from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from .db import init_db, create_user, get_user_by_email, update_user_qdrant_id
from .face_engine import detect_and_embed, upsert_face_embedding
import base64
import numpy as np
import cv2



app = FastAPI(title="Face Recognition API")


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


@app.post("/signup")
def signup(data: SignupRequest):
    existing = get_user_by_email(data.email)
    if existing:
        return {"success": False, "message": "Email already exists"}

    # bcrypt only supports 72 chars
    password = data.password[:72]
    password_hash = bcrypt.hash(password)

    user_id = create_user(
        name=data.name,
        email=data.email,
        password_hash=password_hash
    )

    return {
        "success": True,
        "message": "Signup successful",
        "user_id": user_id
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)
    if not user:
        return {"success": False, "message": "User not found"}

    if not bcrypt.verify(data.password, user["password_hash"]):
        return {"success": False, "message": "Invalid password"}

    return {
        "success": True,
        "message": "Login successful",
        "user_id": user["id"]
    }



# ===============================
# FILE UPLOAD API (REAL WORLD)

@app.post("/register-face-file")
async def register_face_file(
    email: str,
    image: UploadFile = File(...)
):
    file_bytes = await image.read()

    # Convert image → Base64
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

    # 🔍 DEBUG (SEE BASE64 CONVERSION)
    print("✅ Image converted to Base64")
    print("Base64 length:", len(image_base64))
    print("Base64 preview:", image_base64[:60])

    # Reuse base64 registration logic
    return register_face_from_base64(
        email=email,
        image_base64=image_base64
    )


# ===============================
# COMMON FACE REGISTRATION LOGIC
# ===============================
def register_face_from_base64(email: str, image_base64: str):
    user = get_user_by_email(email)
    if not user:
        return {"success": False, "message": "User not found"}

    img_bytes = base64.b64decode(image_base64)
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return {"success": False, "message": "Invalid image"}

    results = detect_and_embed(img)
    if not results:
        return {"success": False, "message": "No face detected"}

    _, _, _, _, emb = results[0]

    upsert_face_embedding(
        user_id=user["id"],
        name=user["name"],
        email=user["email"],
        embedding=emb
    )

    update_user_qdrant_id(user["id"], "registered")

    return {"success": True, "message": "Face registered successfully"}