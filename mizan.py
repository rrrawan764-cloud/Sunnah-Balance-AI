import cv2
import mediapipe as mp

# استخدام الوصول المباشر للمكتبات لتفادي AttributeError
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# إعداد الفيديو (تأكدي أن الملف prayer_test.mp4 موجود في المجلد)
cap = cv2.VideoCapture('prayer_test.mp4')

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # معالجة الصورة
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # رسم الهيكل العظمي إذا تم رصده
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Mizan Al-Sunnah AI', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
