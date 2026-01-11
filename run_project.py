import cv2
import mediapipe as mp

# استخدام الطريقة المباشرة والأكثر استقراراً
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()
cap = cv2.VideoCapture('human_test.mp4')

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('Sunnah Project', frame)
    if cv2.waitKey(1) & ord('q') == 27: break # اضغطي Esc أو q للخروج

cap.release()
cv2.destroyAllWindows()
