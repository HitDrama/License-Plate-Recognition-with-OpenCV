# 🚗 License-Plate-Recognition-with-OpenCV

A powerful project using **OpenCV** and **Deep Learning techniques** to detect, extract, and recognize vehicle license plates from images.  
Designed for fast, accurate and scalable plate recognition.

---

## 📚 Core Libraries Used

- **OpenCV-Python**: Image processing and transformations.
- **EasyOCR**: Optical Character Recognition (OCR) to read text from plates.
- **PyTesseract**: Additional OCR fallback (if needed).
- **Flask**: Web application framework.
- **NumPy**: Matrix operations and image array manipulation.
- **imutils**: Image contour utilities.
- **gTTS**: Convert text to speech (optional).
- **PySpellChecker**: Spell checking extracted text.
- **Googletrans (4.0.0-rc1)**: Translating between English and Vietnamese.
- **PyVi**: Vietnamese language processing.

---

## 🚀 Project Features

- Detect and extract license plate regions from vehicle images.
- OCR extracted plates using EasyOCR.
- Filter and clean plate text (remove noise characters).
- Apply regex to validate and extract standard license plate formats.
- Multiple methods for plate detection:
  - **Contour-based detection**
  - **Morphological operations**
  - **Full-image OCR scanning** fallback
- Save and export detection results automatically.

---

## 📷 Image Processing Workflow

The system processes images through **5 main steps**:  

### 1. Convert Image to Grayscale
- Make the image ready for edge detection and morphology.  
<img src="https://raw.githubusercontent.com/HitDrama/License-Plate-Recognition-with-OpenCV/main/static/train/anh-xam.png" alt="Grayscale Image" width="500">
### 2. Image Smoothing and Noise Reduction
- Apply Gaussian Blur and Bilateral Filter to reduce noise.

<img src="https://github.com/HitDrama/License-Plate-Recognition-with-OpenCV/blob/main/static/train/anh-mo.png" alt="Grayscale Image" width="500">

### 3. Edge Detection (Canny Detection)
- Find edges that potentially form the license plate boundaries.

<img src="https://github.com/HitDrama/License-Plate-Recognition-with-OpenCV/blob/main/static/train/anh-phat-canh.png" alt="Grayscale Image" width="500">

### 4. Contour Detection or Morphological Transformation
- Detect plate region candidates based on shape and aspect ratio.

<img src="https://github.com/HitDrama/License-Plate-Recognition-with-OpenCV/blob/main/static/train/anh-duong-vien.png" alt="Grayscale Image" width="500">

### 5. License Plate Extraction and OCR Result
- Extract plate region, apply OCR, clean text and validate plate format.

<img src="https://github.com/HitDrama/License-Plate-Recognition-with-OpenCV/blob/main/static/train/ket-qua.png" alt="Grayscale Image" width="500">


---

## ⚙️ Setup Instructions
```bash
git clone https://github.com/HitDrama/License-Plate-Recognition-with-OpenCV.git
cd License-Plate-Recognition-with-OpenCV
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000/ or http://127.0.0.1:5000/bienso
```
---

##✨ Developer
-- Built with ❤️ by Đặng Tố Nhân

