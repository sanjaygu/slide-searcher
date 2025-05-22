from pptx import Presentation
import os
from PIL import Image
import io
from typing import List, Dict, Any
import tempfile
import subprocess

class SlideRenderer:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def render_slides(self, pptx_path: str) -> List[str]:
        """
        Render slides to images and return paths to rendered images.
        """
        if not os.path.exists(pptx_path):
            raise FileNotFoundError(f"File not found: {pptx_path}")

        # Convert PPTX to PDF first using LibreOffice
        pdf_path = self._convert_to_pdf(pptx_path)
        
        # Render PDF pages to images
        rendered_paths = self._render_pdf_pages(pdf_path)
        
        # Clean up temporary PDF
        os.remove(pdf_path)
        
        return rendered_paths

    def _convert_to_pdf(self, pptx_path: str) -> str:
        """Convert PPTX to PDF using LibreOffice."""
        # Create temporary PDF file
        pdf_path = os.path.join(tempfile.gettempdir(), f"temp_{os.path.basename(pptx_path)}.pdf")
        
        # Use LibreOffice to convert PPTX to PDF
        try:
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(pdf_path),
                pptx_path
            ], check=True)
            
            # LibreOffice creates the PDF in the same directory as the input file
            temp_pdf = os.path.splitext(pptx_path)[0] + '.pdf'
            os.rename(temp_pdf, pdf_path)
            
            return pdf_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to convert PPTX to PDF: {str(e)}")
        except FileNotFoundError:
            raise Exception("LibreOffice not found. Please install LibreOffice.")

    def _render_pdf_pages(self, pdf_path: str) -> List[str]:
        """Render PDF pages to images."""
        import fitz  # PyMuPDF
        
        pdf_document = fitz.open(pdf_path)
        rendered_paths = []
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
            
            output_path = os.path.join(
                self.output_dir,
                f"slide_{page_num + 1}.png"
            )
            
            pix.save(output_path)
            rendered_paths.append(output_path)
        
        pdf_document.close()
        return rendered_paths

    def _get_slide_dimensions(self, presentation: Presentation) -> Dict[str, int]:
        """Get slide dimensions from presentation."""
        return {
            'width': presentation.slide_width,
            'height': presentation.slide_height
        } 