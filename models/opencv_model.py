import os
import cv2
import uuid
from config import Config

class ImageOpencv:
    def __init__(self,upload_folder=Config.UPLOAD_FOLDER):
        self.upload_folder=upload_folder

    def generate_filename(self,prefix):
        unique=str(uuid.uuid4())[:8]
        return os.path.join(self.upload_folder,f"{prefix}_{unique}.jpg")

    def process_image(self, image_path):
        # Đọc ảnh
        img = cv2.imread(image_path)

        # Chuyển ảnh sang màu xám
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        
        # Tạo tên file mới cho ảnh xám
        filename = self.generate_filename("gray")        
        # Lưu ảnh xám vào thư mục tĩnh
        cv2.imwrite(filename, gray)

        #làm mờ ảnh
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        blur_path = self.generate_filename("blur")
        cv2.imwrite(blur_path, blur)
        
        #phát hiện cạnh 
        edge= cv2.Canny(blur,50,150)
        edge_path = self.generate_filename("edge")
        cv2.imwrite(edge_path, edge)

        #Tìm đường viền
        contours,_= cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        img_contour = img.copy()
        cv2.drawContours(img_contour, contours, -1, (0,255,0), 3)
        contour_path = self.generate_filename("contour")
        cv2.imwrite(contour_path, img_contour)

        # Trả về đường dẫn tương đối đến thư mục static
        return [filename,blur_path,edge_path,contour_path]
