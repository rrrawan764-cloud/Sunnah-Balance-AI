import cv2
import mediapipe as mp
import numpy as np

# إعداد أدوات الرسم والحلول
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0: angle = 360-angle
    return angle

# تأكدي من اسم الفيديو الموجود عندك
video_path = 'prayer_test.mp4' 
cap = cv2.VideoCapture(video_path)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            
            # إحداثيات الجانب الأيسر
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            angle = calculate_angle(shoulder, hip, knee)

            # منطق الألوان والحالة
            if 75 < angle < 105:
                feedback, color = "Correct Rukoo", (0, 255, 0)
            elif angle > 160:
                feedback, color = "Standing Straight", (255, 255, 255)
            else:
                feedback, color = "Adjust Posture", (0, 0, 255)

            # رسم مستطيل الخلفية والنصوص
            cv2.rectangle(image, (0,0), (300, 100), (0,0,0), -1)
            cv2.putText(image, f"Angle: {int(angle)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv2.putText(image, feedback, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        except:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Mizan AI', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
