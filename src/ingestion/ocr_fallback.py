import pytesseract
from PIL import Image
from typing import Dict, Any, List
import os
import cv2
import numpy as np

class OCRProcessor:
    def __init__(self, config_path: str = "config/ocr_config.json"):
        self.tesseract_config = '--oem 3 --psm 6'
        self._load_config(config_path)

    def _load_config(self, config_path: str):
        """Load OCR configuration."""
        # Default configuration
        self.config = {
            'preprocessing': {
                'resize': True,
                'denoise': True,
                'threshold': True
            },
            'languages': ['eng'],
            'confidence_threshold': 0.6
        }
        
        if os.path.exists(config_path):
            import json
            with open(config_path, 'r') as f:
                self.config.update(json.load(f))

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process an image using OCR to extract text.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            # Read image
            image = cv2.imread(image_path)
            
            # Preprocess image
            processed_image = self._preprocess_image(image)
            
            # Convert to PIL Image for pytesseract
            pil_image = Image.fromarray(processed_image)
            
            # Perform OCR
            text = pytesseract.image_to_string(
                pil_image,
                config=self.tesseract_config,
                lang='+'.join(self.config['languages'])
            )
            
            # Get confidence scores
            data = pytesseract.image_to_data(
                pil_image,
                config=self.tesseract_config,
                lang='+'.join(self.config['languages']),
                output_type=pytesseract.Output.DICT
            )
            
            confidence = self._calculate_confidence(data)
            
            return {
                'text': text,
                'confidence': confidence,
                'image_path': image_path,
                'words': self._extract_words_with_confidence(data)
            }
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results."""
        if self.config['preprocessing']['resize']:
            image = cv2.resize(image, None, fx=2, fy=2)
        
        if self.config['preprocessing']['denoise']:
            image = cv2.fastNlMeansDenoisingColored(image)
        
        if self.config['preprocessing']['threshold']:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        return image

    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for OCR results."""
        confidences = [float(conf) for conf in data['conf'] if conf != '-1']
        return np.mean(confidences) / 100 if confidences else 0.0

    def _extract_words_with_confidence(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract words with their confidence scores and positions."""
        words = []
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                words.append({
                    'text': data['text'][i],
                    'confidence': float(data['conf'][i]) / 100,
                    'position': {
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    }
                })
        return words 