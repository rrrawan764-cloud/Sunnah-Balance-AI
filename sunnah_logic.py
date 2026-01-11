import cv2
import mediapipe as mp
import numpy as np

# دالة حساب الزاوية بين ثلاث نقاط
def calculate_angle(a, b, c):
    a = np.array(a) # الكتف
    b = np.array(b) # الحوض
    c = np.array(c) # الركبة
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture('human_test.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('prayer_analysis.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

print("⏳ جاري تحليل زوايا الصلاة...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # استخراج إحداثيات الكتف والحوض والركبة (الجانب الأيسر كمثال)
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        
        # حساب الزاوية
        angle = calculate_angle(shoulder, hip, knee)
        
        # عرض الزاوية على الفيديو
        cv2.putText(frame, f"Back Angle: {int(angle)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if 80 < angle < 100 else (0, 0, 255), 2)
        
        # رسم الهيكل
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    out.write(frame)

cap.release()
out.release()
print("✅ تم التحليل! افتحي الملف: prayer_analysis.mp4")
