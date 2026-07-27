"""
test_camera.py — Week 1 first test.
Run this FIRST to confirm camera is working.
Usage: python test_camera.py
Press Q to quit.
"""
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

print(f"Camera opened : {cap.isOpened()}")
print(f"Width         : {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
print(f"Height        : {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"FPS           : {cap.get(cv2.CAP_PROP_FPS)}")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame grab failed")
        break
    cv2.imshow("Arducam UC852 — Color Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
