import numpy as np
import cv2

class OCRExtractor:
    def __init__(self, use_easyocr=False):
        """
        OCR Extractor that can use EasyOCR or Tesseract
        """
        self.use_easyocr = use_easyocr

        if self.use_easyocr:
            try:
                import easyocr
                self.reader = easyocr.Reader(['en'])
                self.engine = "easyocr"
            except ImportError:
                raise ImportError("EasyOCR not installed. Run: pip install easyocr")
        else:
            try:
                import pytesseract
                self.reader = pytesseract
                self.engine = "tesseract"
            except ImportError:
                raise ImportError("Pytesseract not installed. Run: pip install pytesseract")

    def preprocess_image(self, image):
        """
        Preprocess image for better OCR accuracy
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        return thresh

    def extract_text(self, image):
        """
        Extract text from image
        """
        processed = self.preprocess_image(image)

        if self.engine == "easyocr":
            result = self.reader.readtext(processed)
            text = " ".join([item[1] for item in result])
        else:
            text = self.reader.image_to_string(processed)

        return text.strip()