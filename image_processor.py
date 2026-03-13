import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    def __init__(self):
        self.target_size = (800, 800)  # Max dimensions
        
    def preprocess(self, image):
        """Main preprocessing pipeline"""
        # Convert PIL to OpenCV
        if isinstance(image, Image.Image):
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Apply preprocessing steps
        image = self.resize_image(image)
        image = self.convert_to_grayscale(image)
        image = self.denoise(image)
        image = self.enhance_contrast(image)
        image = self.threshold(image)
        
        return image
    
    def resize_image(self, image):
        """Resize while maintaining aspect ratio"""
        h, w = image.shape[:2]
        
        if h > self.target_size[0] or w > self.target_size[1]:
            scale = min(self.target_size[0]/h, self.target_size[1]/w)
            new_size = (int(w*scale), int(h*scale))
            image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        
        return image
    
    def convert_to_grayscale(self, image):
        """Convert to grayscale if needed"""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    def denoise(self, image):
        """Remove noise while preserving edges"""
        return cv2.fastNlMeansDenoising(image, None, 30, 7, 21)
    
    def enhance_contrast(self, image):
        """Apply CLAHE for better contrast"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(image)
    
    def threshold(self, image):
        """Adaptive thresholding for better text extraction"""
        return cv2.adaptiveThreshold(
            image, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
    
    def detect_equation_region(self, image):
        """Detect and crop equation region"""
        # Find contours
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        if contours:
            # Get largest contour (assumed to be equation)
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            
            # Add padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2*padding)
            h = min(image.shape[0] - y, h + 2*padding)
            
            return image[y:y+h, x:x+w]
        
        return image
    
    def image_to_bytes(self, image):
        """Convert OpenCV image to bytes for API"""
        if isinstance(image, np.ndarray):
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            _, buffer = cv2.imencode('.jpg', image)
            return buffer.tobytes()
        return None