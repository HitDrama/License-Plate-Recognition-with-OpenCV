import os # Thư viện xử lý đường dẫn, file và thư mục
import uuid # Thư viện tạo UUID để đặt tên file duy nhất
from flask import render_template, request, flash # Import các hàm Flask để render HTML, nhận request, và thông báo
from werkzeug.utils import secure_filename # Hàm bảo mật tên file upload
from forms.form_opencv import UploadForm # Import form để upload file từ người dùng
from models.Bienso_model import BienSoXe # Import class xử lý nhận diện biển số xe
from config import Config # Import cấu hình, ví dụ đường dẫn upload
from gtts import gTTS # Thư viện chuyển văn bản thành giọng nói (Google Text-to-Speech)
import uuid

plate_recognition = BienSoXe()

audio_cache = {}

def Biensoxe():
    form = UploadForm()   # Tạo một instance của form để nhận file từ người dùng
    plate_text = "Không nhận dạng được"   # Giá trị mặc định khi chưa nhận diện được biển số
    image = ""    # Đường dẫn hình ảnh để render về giao diện
    audio_file = ""   # Đường dẫn file âm thanh để phát lại kết quả nhận diện

    # Kiểm tra nếu form được submit hợp lệ (POST + dữ liệu hợp lệ)
    if form.validate_on_submit():
        file = request.files.get("file")    # Lấy file từ request gửi từ người dùng
        
        # Kiểm tra file có tồn tại và tên file không rỗng
        if file and file.filename:
                # Tạo đường dẫn lưu file upload an toàn
                filepath = os.path.join(Config.UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(filepath)   # Lưu file vào thư mục chỉ định
                
                # Xử lý ảnh để nhận diện biển số, trả về đường dẫn ảnh và kết quả nhận diện
                image, plate_text = plate_recognition.xu_ly_anh(filepath)
                
                # Nếu nhận diện thành công (không phải chuỗi mặc định)
                if plate_text != "Không nhận dạng được":
                    # Kiểm tra biển số này đã có audio chưa
                    if plate_text not in audio_cache:
                                os.makedirs("static/audio", exist_ok=True)    # Tạo thư mục audio nếu chưa tồn tại
                                
                                # Tạo tên file âm thanh duy nhất (dùng UUID và thay khoảng trắng)
                                filename = f"{plate_text.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.mp3"
                                audio_path = os.path.join("static", "audio", filename)    # Đường dẫn đầy đủ
                                # Tạo file âm thanh từ văn bản (tiếng Việt)
                                gTTS(text=f"Biển số xe là {plate_text}", lang='vi').save(audio_path)
                                # Lưu đường dẫn tương đối vào cache
                                audio_cache[plate_text] = f"audio/{filename}"
                    
                    # Lấy đường dẫn file âm thanh từ cache để gửi về giao diện
                    audio_file = audio_cache[plate_text]
                    # Gửi thông báo thành công kèm nội dung biển số
                    flash(f"Nhận diện thành công: {plate_text}", "success")

    # Render template HTML và gửi dữ liệu về giao diện
    return render_template("Bienso.html", form=form, image=image, plate_text=plate_text, audio_file=audio_file)
