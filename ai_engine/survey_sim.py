import cv2
from ultralytics import YOLO
import requests

# 1. Load the AI Model
# Using yolov8n.pt for high-speed detection (YOLO26 logic)
model = YOLO('yolov8n.pt') 

# 2. Your API URL
# Since you are running Docker locally, use http://localhost:8000
# If using a server/ngrok, replace this URL
API_URL = "http://localhost:8000/verify"

# 3. Access Camera (0 is default webcam)
cap = cv2.VideoCapture(0)

print("--- A-MAORM Survey System Live ---")

while cap.isOpened():
    success, frame = cap.read()
    if not success: 
        break

    # 4. AI Detection
    results = model(frame, verbose=False) 

    for r in results:
        for box in r.boxes:
            # Class 11 is 'stop sign' in some models, but 'fire hydrant' or others in others.
            # In standard COCO (yolov8n), Billboard isn't a default class. 
            # For this simulation, we will detect 'refrigerator' (72) or 'tv' (62) 
            # to act as a "Billboard" proxy unless you have a custom model.
            
            detected_class = int(box.cls[0])
            
            # Change '62' to the class ID you want to trigger the enforcement
            if detected_class == 62 or detected_class == 11: 
                print("Billboard/Structure Detected!")
                
                # Simulated License/QR and GPS Georeferencing
                simulated_qr = "LIC-2026-001"
                curr_lat, curr_lon = 12.9716, 77.5946 
                
                # 5. Enforcement: Send to Backend
                try:
                    payload = {
                        'lat': curr_lat, 
                        'lon': curr_lon, 
                        'w': 10.5, 
                        'h': 5.2, 
                        'qr_code': simulated_qr
                    }
                    resp = requests.get(API_URL, params=payload, timeout=1)
                    print(f"Enforcement Update: {resp.json()}")
                except Exception as e:
                    print(f"Sync Error: Ensure Docker is running. {e}")

    # 6. Display visual feed
    # We use results[0].plot() to see the AI boxes on screen
    annotated_frame = results[0].plot()
    cv2.imshow("A-MAORM Survey (60km/h)", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()