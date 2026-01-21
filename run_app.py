import uvicorn
from qdrant_client import QdrantClient
from app.db import init_db
from app.fastapi_app import app

def start_qdrant():
    print("🚀 Starting Embedded Qdrant...")
    client = QdrantClient(path="qdrant_data", prefer_grpc=False)
    return client


def main():
    # 1️⃣ Start Qdrant Embedded
    qdrant = start_qdrant()

    # 2️⃣ Initialize PostgreSQL tables
    print("🚀 Checking PostgreSQL...")
    init_db()

    # 3️⃣ Start FastAPI server
    print("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
