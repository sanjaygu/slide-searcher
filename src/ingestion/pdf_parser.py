from PyPDF2 import PdfReader
from typing import List, Dict, Any
import os
import fitz  # PyMuPDF
from PIL import Image
import io

class PDFParser:
    def __init__(self):
        self.supported_extensions = ['.pdf']

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse a PDF file and extract content from each page.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Use PyMuPDF for better image extraction
        pdf_document = fitz.open(file_path)
        pages_data = []

        for idx, page in enumerate(pdf_document, 1):
            page_data = {
                'page_number': idx,
                'text_content': page.get_text(),
                'images': self._extract_images(page),
                'metadata': self._get_page_metadata(page)
            }
            pages_data.append(page_data)

        pdf_document.close()
        return pages_data

    def _extract_images(self, page) -> List[Dict[str, Any]]:
        """Extract images from PDF page using PyMuPDF."""
        images = []
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            
            image_data = {
                'position': img[1:5],  # (x0, y0, x1, y1)
                'image_bytes': image_bytes,
                'format': base_image["ext"]
            }
            images.append(image_data)
        
        return images

    def _get_page_metadata(self, page) -> Dict[str, Any]:
        """Get metadata for the page."""
        return {
            'width': page.rect.width,
            'height': page.rect.height,
            'rotation': page.rotation
        } 