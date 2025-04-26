import os
from flask import render_template, request, flash
from werkzeug.utils import secure_filename
from forms.form_opencv import UploadForm
from models.opencv_model import ImageOpencv
from config import Config

def home():
    image_processor=ImageOpencv()
    form=UploadForm()

    if form.validate_on_submit():
        file=request.files.get("file") #thông tin ảnh upload tên file, size..

        if file and file.filename:
            filename=secure_filename(file.filename) #tên file
            filepath=os.path.join(Config.UPLOAD_FOLDER,filename) #đường dẫn file
            file.save(filepath) #lưu file

            #gọi hàm xử lý ảnh
            xulyanh=image_processor.process_image(filepath)
            flash("File đã được xử lý")
            return render_template("opencv.html",form=form,images=xulyanh)

    return render_template("opencv.html",form=form)