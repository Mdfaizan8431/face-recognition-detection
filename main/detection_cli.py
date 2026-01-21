# app/detection_cli.py
import cv2
from .face_engine import detect_and_embed, search_face
from datetime import datetime
from .db import get_last_event, save_attendance

MIN_GAP_SECONDS = 60 # 1 minutes



def main():
    print("[INFO] Starting face detection...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    THRESHOLD = 0.45  # cosine similarity threshold

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        

        detections = detect_and_embed(frame)
        print("Faces detected:", len(detections))

        for (x1, y1, x2, y2, emb) in detections:
         results = search_face(emb, limit=1)

        name = "Unknown"
        score = None   # ✅ ALWAYS initialize
        score_text = ""   # ✅ ALWAYS define


        if results:
            top = results[0]
            score = getattr(top, "score", None)


            if score is not None and score > THRESHOLD:
                name = top.payload.get("name", "Unknown")


            if score > THRESHOLD:
                user_id = top.payload.get("user_id")
                last_event, last_time = get_last_event(user_id)

                if last_event is None:
                    # First time seen
                    save_attendance(user_id, "ENTRY", score)
                    print("🟢 ENTRY recorded")

                elif last_event == "ENTRY":
                    # Check time gap before EXIT
                    gap = (datetime.now() - last_time).total_seconds()

                    if gap >= MIN_GAP_SECONDS:
                        save_attendance(user_id, "EXIT", score)
                        print("🔴 EXIT recorded")
                    else:
                        print(f"⏳ EXIT blocked (only {int(gap)} sec passed)")

                else:
                    # Last was EXIT → allow ENTRY
                    save_attendance(user_id, "ENTRY", score)
                    print("🟢 ENTRY recorded")

            # Draw rectangle and text
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{name} {score_text}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
