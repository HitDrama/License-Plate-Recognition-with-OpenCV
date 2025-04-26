import os
from flask import render_template, request, flash
from werkzeug.utils import secure_filename
from forms.form_opencv import UploadForm
from config import Config
from models.license_model import LicensePlate 

def license_plate():
    form=UploadForm()
    biensomodel=LicensePlate()
    if form.validate_on_submit():
        file=request.files.get("file")
        if file and file.filename:
            filename=secure_filename(file.filename)
            filepath=os.path.join(Config.UPLOAD_FOLDER,filename)
            file.save(filepath)
            xulyanh,plate_text=biensomodel.process_image(filepath)
            return render_template("license_plate.html",form=form,image=xulyanh,plate_text=plate_text)

    return render_template("license_plate.html",form=form)