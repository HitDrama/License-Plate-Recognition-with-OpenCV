import os
import cv2
import uuid
import numpy as np
import easyocr
import imutils
from config import Config

class LicensePlate:
    def __init__(self,upload_folder=Config.UPLOAD_FOLDER):
        self.upload_folder=upload_folder #đường dẫn lưu ảnh
        self.reader=easyocr.Reader(['en','vi']) #khởi tạo EasyOcr nhận diện ký tự

    def generate_filename(self,prefix):
        #tạo chuỗi ID ngẫu nhiên gồm 8 ký tự
        unique_id=str(uuid.uuid4())[:8]
        return os.path.join(self.upload_folder,f"{prefix}_{unique_id}.jpg")


    def process_image(self,image_path):
        #đoc ảnh
        img=cv2.imread(image_path)
        #chuyển ảnh màu sang ảnh xám (xử lý ảnh dễ hơn)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #làm mờ ảnh
        blur=cv2.GaussianBlur(gray,(5,5),0)
        #phát hiện cạnh
        edge=cv2.Canny(blur,50,150)
        #tìm tất cả đường viền
        contours=cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #chuẩn hóa định dạng contours
        contours=imutils.grab_contours(contours)

        plate_text="Không nhận dạng được"
        #sắp xếp các contours theo diện tích giảm dần, tìm contour lớn nhất => có thể là biển số
        for c in sorted(contours,key=cv2.contourArea,reverse=True):
            #tính chu vi contours
            perimeter=cv2.arcLength(c,True)
            #làm trơn các countour để tìm các góc
            approx=cv2.approxPolyDP(c,0.018*perimeter,True)

            #nếu contour có 4 đỉnh => biển số
            if len(approx)==4:
                #tìm tọa độ và kích thước countour biển số
                x,y,w,h=cv2.boundingRect(approx)
                #cắt vùng có thể là biển số từ ảnh xám
                license_plate=gray[y:y+h,x:x+w]
                #dùng easy ORC tách chữ trên vùng ảnh biển số
                results=self.reader.readtext(license_plate)
                if results:
                  #nối các chuỗi nhận diện => thành 1 chuỗi
                  plate_text=" ".join([res[1]  for res in results])
                
                #vẽ hình chữ nhật bao quanh biển số trên ảnh gốc
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                break

        out_path=self.generate_filename("nhandien")
        cv2.imwrite(out_path,img)

        return out_path, plate_text