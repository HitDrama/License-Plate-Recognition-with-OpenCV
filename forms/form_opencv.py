from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from flask_wtf.file import FileField,FileRequired,FileAllowed,FileSize 
from wtforms.validators import DataRequired, NumberRange

class UploadForm(FlaskForm):
    file=FileField("File",validators=[
        FileRequired(message="Vui lòng chọn file"),
        FileAllowed(['jpg','jpeg','png','gif','mp4','avi','mkv','flv'],"Chỉ cho phép upload file .jpg, jpeg,png,gif,mp4,avi,mkv,flv"),
        FileSize(max_size=1024 * 1024 * 1024)  #10mb
    ])
    submit=SubmitField("Tải lên")