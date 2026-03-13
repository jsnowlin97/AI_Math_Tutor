import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()

import easyocr
import numpy as np

class OCRExtractor:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extract_text(self, image):

        img = np.array(image)

        results = self.reader.readtext(img)

        equation = ""

        for (_, text, conf) in results:
            equation += text + " "

        return equation.strip()
