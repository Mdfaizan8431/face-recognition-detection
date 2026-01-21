# app/face_engine.py
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from qdrant_client import QdrantClient
from qdrant_client import models as qmod
from .config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION, QDRANT_DISTANCE


# -------------------- Load InsightFace model (CPU) --------------------

app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640, 640))   # CPU mode


# ----------------"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Uq5AQKnIFQLJJelt0dZ2nzQ4cemEx-6ImdKph29OTlI"---- Combined Detect + Embed --------------------

def detect_and_embed(frame_bgr):
    """Returns list of (x1, y1, x2, y2, embedding)"""
    faces = app.get(frame_bgr)
    output = []

    for f in faces:
        x1, y1, x2, y2 = f.bbox.astype(int)
        emb = f.embedding
        output.append((x1, y1, x2, y2, emb))

    return output


# -------------------- Qdrant Insert --------------------

def upsert_face_embedding(user_id, name, email, embedding):
    """Save embedding to Qdrant"""
    ensure_qdrant_collection()

    vector = embedding.tolist()

    payload = {
        "user_id": user_id,
        "name": name,
        "email": email,
    }

    qdrant.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[{
            "id": int(user_id),
            "vector": vector,
            "payload": payload
        }]
    )

# -------------------- Qdrant Setup --------------------

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=False
)

def ensure_qdrant_collection():
    collections = qdrant.get_collections().collections
    collection_names = [c.name for c in collections]

    if QDRANT_COLLECTION not in collection_names:
        qdrant.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=qmod.VectorParams(
                size=512,
                distance=qmod.Distance.COSINE,
            ),
        )
        print(f"➕ Created Qdrant collection `{QDRANT_COLLECTION}`")
    else:
        print(f"✔ Qdrant collection `{QDRANT_COLLECTION}` already exists")


# -------------------- Qdrant Search --------------------

def search_face(embedding: np.ndarray, limit: int = 1):
    ensure_qdrant_collection()

    try:
        res = qdrant.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=embedding.tolist(),
            limit=limit,
        )
        return res

    except Exception as e:
        print("[QDRANT ERROR]", e)
        return []
