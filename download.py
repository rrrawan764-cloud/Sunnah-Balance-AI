cat <<EOF > run_project.py
import cv2
import mediapipe as mp

# إعداد مكتبة MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# فتح الفيديو الجديد الذي حملناه
cap = cv2.VideoCapture('human_test.mp4')

print("بدأت المعالجة... اضغطي حرف 'q' في نافذة الفيديو للإغلاق")

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    # تحويل الصورة لـ RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # رسم الهيكل العظمي إذا وجد شخصاً في الفيديو
    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            img, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
        )

    # عرض الفيديو
    cv2.imshow("Sunnah Project - Pose Estimation", img)
    
    # الخروج عند الضغط على q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
EOF
