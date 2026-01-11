import cv2
# استيراد المكونات مباشرة من المسار العميق للمكتبة
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

# تجهيز المحرك
pose_engine = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5
)

cap = cv2.VideoCapture('human_test.mp4')

# إعدادات حفظ الفيديو
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
w, h = int(cap.get(3)), int(cap.get(4))
out = cv2.VideoWriter('output_result.mp4', fourcc, fps, (w, h))

print("⏳ جاري تحليل الفيديو ورسم الهيكل العظمي...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # المعالجة
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_engine.process(frame_rgb)
    
    # رسم النقاط (33 نقطة تتبع)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS
        )
    
    out.write(frame)

cap.release()
out.release()
print("✅ اكتملت العملية! الملف الجديد هو: output_result.mp4")
