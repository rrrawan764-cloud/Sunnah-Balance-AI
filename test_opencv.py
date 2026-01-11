import cv2

cap = cv2.VideoCapture('human_test.mp4')

if not cap.isOpened():
    print("❌ لا يمكن العثور على الفيديو!")
else:
    print("✅ تم العثور على الفيديو، حاول البحث عن نافذة بعنوان 'Sunnah Test'")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("انتهى الفيديو.")
        break
    
    cv2.imshow('Sunnah Test', frame)
    
    # انتظر 25 مللي ثانية لكل إطار، واخرج إذا ضغطت q
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("تم إغلاق البرنامج بنجاح.")
