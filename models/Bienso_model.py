import os # Thư viện thao tác với hệ thống file (tạo đường dẫn, kiểm tra file...)
import cv2 # Thư viện xử lý ảnh OpenCV
import uuid  # Dùng để tạo ID duy nhất (giúp đặt tên file không bị trùng)
import numpy as np  # Xử lý ma trận, ảnh dạng số
import imutils # Hỗ trợ thao tác ảnh như tìm contour, resize tiện lợi hơn OpenCV thuần
import easyocr # Thư viện OCR nhận diện chữ trên ảnh
import re # Thư viện regex (dùng để tìm mẫu chuỗi giống biển số)
from config import Config # Import file cấu hình, chứa thông tin như đường dẫn thư mục lưu file

class BienSoXe: # Lớp xử lý nhận diện biển số từ ảnh
    def __init__(self, thu_muc_luu=Config.UPLOAD_FOLDER): # Hàm khởi tạo, nhận tham số thư mục lưu ảnh
        self.thu_muc_luu = thu_muc_luu # Gán thư mục lưu vào thuộc tính của lớp
        self.reader = easyocr.Reader(['en', 'vi']) # Khởi tạo easyocr hỗ trợ tiếng Anh và Việt (nhận diện chữ trên ảnh)

    def tao_ten_file(self, tien_to): # Tạo tên file duy nhất với tiền tố tien_to
        return os.path.join(self.thu_muc_luu, f"{tien_to}_{uuid.uuid4().hex[:8]}.jpg") # Tạo tên file có 8 ký tự random

    def loc_chuoi_bien_so(self, chuoi): # Làm sạch chuỗi ký tự, chỉ giữ các ký tự hợp lệ cho biển số
        ky_tu_hop_le = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-. ") # Tập ký tự hợp lệ: chữ cái, số, dấu chấm/gạch
        chuoi_sach = ''.join(e for e in chuoi.upper() if e in ky_tu_hop_le) # Lọc từng ký tự, chỉ giữ ký tự hợp lệ
        return chuoi_sach if chuoi_sach.strip() else "Khong nhan dien duoc" # Nếu chuỗi sau khi lọc không rỗng thì trả về, ngược lại báo lỗi

    def trich_so_bien(self, chuoi_day_du): # Tìm chuỗi biển số chuẩn trong đoạn text bằng regex
        mau = r'\b\d{2}-[A-Z]\d\s?\d{4,5}\b' # Mẫu biển số hợp lệ: 2 số - 1 chữ + 1 số + 4-5 số
        ket_qua = re.search(mau, chuoi_day_du.upper()) # Tìm chuỗi khớp mẫu trong text (chuyển về in hoa)
        if ket_qua:
            return ket_qua.group() # Nếu có, trả về chuỗi khớp
        phan = chuoi_day_du.strip().split() # Nếu không, cắt chuỗi thành danh sách từ
        return ' '.join(phan[:2]) if len(phan) >= 2 else chuoi_day_du.strip() # Lấy 2 từ đầu tiên nếu đủ, không thì trả lại toàn bộ text

    def ocr_va_loc(self, anh, do_tin_cay_min=0.4, do_dai_min=4): # Chạy OCR trên ảnh và lọc kết quả tin cậy
        ket_qua = self.reader.readtext(anh) # Chạy OCR với easyocr, trả về list [bbox, text, prob]
        ket_qua_hop_le = [(bbox, text, prob) for bbox, text, prob in ket_qua if prob >= do_tin_cay_min and len(text.strip()) >= do_dai_min] # Lọc kết quả theo độ tin cậy và độ dài text
        if ket_qua_hop_le: # Nếu có kết quả hợp lệ
            ket_qua_hop_le.sort(key=lambda x: min(pt[1] for pt in x[0])) # Sắp xếp từ trên xuống dưới theo tọa độ y nhỏ nhất
            chuoi_ghep = ' '.join(self.loc_chuoi_bien_so(text) for _, text, _ in ket_qua_hop_le) # Làm sạch và ghép tất cả chuỗi lại
            bien_so = self.trich_so_bien(chuoi_ghep) # Lọc ra biển số từ chuỗi ghép
            return bien_so.strip() # Trả về biển số
        return None # Không có kết quả hợp lệ, trả về None

    # def tim_bien_theo_contour(self, anh, xam): # Tìm biển số bằng cách phát hiện contour (đường viền hình học)
    #     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) # Tăng tương phản ảnh bằng CLAHE
    #     tang_anh = clahe.apply(cv2.equalizeHist(xam)) # Áp dụng CLAHE
    #     anh_muot = cv2.bilateralFilter(tang_anh, 11, 17, 17) # Làm mịn ảnh, giảm nhiễu
    #     canh = cv2.Canny(anh_muot, 50, 150) # Tìm cạnh ảnh bằng Canny Edge Detection
    #     contours = imutils.grab_contours(cv2.findContours(canh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)) # Tìm contour từ ảnh cạnh
    #     for c in sorted(contours, key=cv2.contourArea, reverse=True)[:15]: # Lọc 15 contour lớn nhất
    #         approx = imutils.grab_contours(cv2.findContour(canh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
    #         if 4 <= len(approx) <= 6: #  lấy 4-6 đỉnh(canh)
    #             x , y , w, h = cv2.barcodeArea(approx)
    #             if 0.8 <= w / h <= 7.0 and 0.005 <= (w * h) / (anh.shape[0] * anh.shape[1]) <= 0.5: # Kiểm tra tỉ lệ khung hình và kích thước vùng so với toàn ảnh
    #                 vung_bien = xam[y-5:y+h+5, x-5:x+w+5] # Cắt vùng ảnh nghi ngờ chứa biển số
    #                 bien_phong_to = cv2.resize(vung_bien, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR) # Phóng to ảnh biển số
    #                 text = self.ocr_va_loc(bien_phong_to) # Nhận diện chữ trên vùng biển số
    #                 if text: # Nếu nhận diện được
    #                     cv2.rectangle(anh, (x, y), (x + w, y + h), (0, 255, 0), 2) # Vẽ khung xanh quanh biển số
    #                     cv2.putText(anh, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) # Ghi text biển số lên ảnh
    #                     return text # Trả về biển số
    #     return None # Không tìm thấy biển số

    def tim_bien_theo_contour(self, anh, xam):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        xam = clahe.apply(cv2.equalizeHist(xam))
        anh_muot = cv2.GaussianBlur(xam, (5, 5), 0)
        anh_muot = cv2.bilateralFilter(anh_muot, 11, 75, 75)
        canh = cv2.Canny(anh_muot, 50, 150)
        contours = imutils.grab_contours(cv2.findContours(canh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
        
        for c in sorted(contours, key=cv2.contourArea, reverse=True)[:15]:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if 4 <= len(approx) <= 6:
                x, y, w, h = cv2.boundingRect(approx)
                if 0.8 <= w / h <= 7.0 and 0.005 <= (w * h) / (anh.shape[0] * anh.shape[1]) <= 0.5:
                    vung_bien = xam[y-10:y+h+10, x-10:x+w+10]
                    bien_phong_to = cv2.resize(vung_bien, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
                    text = self.ocr_va_loc(bien_phong_to, do_tin_cay_min=0.3)
                    if text:
                        cv2.rectangle(anh, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(anh, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        return text
        return None
    
    def tim_bien_theo_hinh_thai(self, anh, xam):    # Tìm biển số bằng phương pháp hình thái học (morphology)
        sobel = cv2.Sobel(xam, cv2.CV_8U, 1, 0, ksize=3)      # Tính gradient theo trục x (cạnh dọc)
        _, nguong = cv2.threshold(sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)     # Nhị phân hóa bằng Otsu
        morph = cv2.morphologyEx(nguong, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3)))     # Morph close để nối liền các vùng chữ

        contours = imutils.grab_contours(cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))     # Tìm contour sau morph
        for c in sorted(contours, key=cv2.contourArea, reverse=True)[:5]:     # Xét 5 contour lớn nhất
            x, y, w, h = cv2.boundingRect(c)     # Lấy bounding box
            if 1.0 <= w / h <= 6.0:      # Kiểm tra tỉ lệ khung hình
                vung = xam[y-5:y+h+5, x-5:x+w+5]     # Cắt ảnh nghi ngờ chứa biển số
                vung_phong_to = cv2.resize(vung, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)   # Phóng to
                text = self.ocr_va_loc(vung_phong_to, do_tin_cay_min=0.3)    # Nhận diện chữ
                if text:
                    cv2.rectangle(anh, (x, y), (x + w, y + h), (0, 0, 255), 2)      # Vẽ khung đỏ
                    cv2.putText(anh, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)      # Ghi text lên ảnh
                    return text     # Trả về biển số
        return None       # Không tìm thấy
    

    def quet_toan_bo_anh(self, anh, xam): # Quét toàn bộ ảnh bằng OCR, dùng khi không tìm được contour
        ket_qua = self.reader.readtext(xam) # OCR toàn ảnh
        ket_qua_hop_le = [(bbox, text, prob) for bbox, text, prob in ket_qua if prob >= 0.3 and len(text.strip()) >= 4] # Lọc kết quả tin cậy

        if ket_qua_hop_le:
            ket_qua_hop_le.sort(key=lambda x: min(pt[1] for pt in x[0])) # Sắp xếp theo y
            chuoi_ghep = ' '.join(self.loc_chuoi_bien_so(text) for _, text, _ in ket_qua_hop_le) # Làm sạch
            bien_so = self.trich_so_bien(chuoi_ghep)

            bbox = ket_qua_hop_le[0][0] # Lấy bbox đầu tiên
            diem = np.array(bbox, np.int32).reshape((-1, 1, 2)) # Định dạng lại bbox
            cv2.polylines(anh, [diem], True, (255, 0, 0), 2) # Vẽ khung xanh dương
            x_min, y_min = min(p[0] for p in bbox), min(p[1] for p in bbox)
            cv2.putText(anh, bien_so, (int(x_min), int(y_min - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2) # Ghi text
            return bien_so.strip()
        return None
    def xu_ly_anh(self, duong_dan_anh): # Hàm chính xử lý ảnh đầu vào
        anh = cv2.imread(duong_dan_anh) # Đọc ảnh
        if anh is None:
            return None, "Khong the doc anh" # Lỗi đọc ảnh
        xam = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY) # Chuyển sang ảnh xám

        for phuong_phap in [self.tim_bien_theo_contour, self.tim_bien_theo_hinh_thai, self.quet_toan_bo_anh]: # Thử từng phương pháp
            try:
                text = phuong_phap(anh, xam)
                if text:
                    duong_dan_kq = self.tao_ten_file("detected")
                    cv2.imwrite(duong_dan_kq, anh) # Lưu ảnh kết quả
                    return duong_dan_kq, text # Trả kết quả
            except Exception as e:
                print(f"Loi trong {phuong_phap.__name__}: {e}") # Log lỗi nếu có

        duong_dan_kq = self.tao_ten_file("detected")
        cv2.imwrite(duong_dan_kq, anh)
        return duong_dan_kq, "Khong nhan dien duoc" # Không tìm được



