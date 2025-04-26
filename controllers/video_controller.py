import os
import cv2
from flask import Response, render_template
from config import Config

video_stream = None

def generate_frames():
    global video_stream
    video_stream = cv2.VideoCapture(0)  # Mở webcam
    while True:
        success, frame = video_stream.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_byte = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n\r\n' + frame_byte + b'\r\n'
               )

def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_page():
    return render_template("video.html")


def record_video():
    global video_stream
    if not video_stream or not video_stream.isOpened():
        return "Webcam chưa được mở."

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_path = os.path.join(Config.VIDEO_FOLDER, "ghi_video.avi")
    
    # Đảm bảo có dấu phẩy giữa các tham số
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (720, 640))

    # Quay video trong 100 frame (hoặc có thể thay đổi tùy theo yêu cầu)
    for _ in range(100):
        success, frame = video_stream.read()
        if not success:
            break
        out.write(frame)

    out.release()  # Đóng file sau khi quay xong
    video_stream.release()  # Giải phóng webcam khi không cần thiết nữa

    return "Video đã được ghi lại thành công."

