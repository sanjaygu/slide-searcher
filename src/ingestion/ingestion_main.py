import os
from typing import List, Dict, Any
from pptx_parser import PPTXParser
from pdf_parser import PDFParser
from ocr_fallback import OCRProcessor
from slide_renderer import SlideRenderer

class DocumentIngestionPipeline:
    def __init__(self, upload_dir: str, output_dir: str):
        self.upload_dir = upload_dir
        self.output_dir = output_dir
        self.pptx_parser = PPTXParser()
        self.pdf_parser = PDFParser()
        self.ocr_processor = OCRProcessor()
        self.slide_renderer = SlideRenderer(os.path.join(output_dir, "rendered_images"))
        
        # Create necessary directories
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "rendered_images"), exist_ok=True)

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document (PPTX or PDF) and return extracted data.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Parse document based on type
        if file_ext in self.pptx_parser.supported_extensions:
            slides_data = self.pptx_parser.parse(file_path)
            rendered_paths = self.slide_renderer.render_slides(file_path)
        elif file_ext in self.pdf_parser.supported_extensions:
            slides_data = self.pdf_parser.parse(file_path)
            # For PDFs, we'll use the first page as the rendered image
            rendered_paths = [file_path]  # You might want to implement PDF rendering
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

        # Process each slide
        processed_data = []
        for idx, (slide_data, rendered_path) in enumerate(zip(slides_data, rendered_paths)):
            # If no text content, try OCR
            if not slide_data.get('text_content'):
                ocr_result = self.ocr_processor.process_image(rendered_path)
                slide_data['text_content'] = ocr_result['text']
                slide_data['ocr_confidence'] = ocr_result['confidence']

            processed_data.append({
                'slide_number': idx + 1,
                'content': slide_data.get('text_content', ''),
                'images': slide_data.get('images', []),
                'notes': slide_data.get('notes', ''),
                'rendered_image': rendered_path,
                'metadata': {
                    'layout': slide_data.get('layout', ''),
                    'ocr_confidence': slide_data.get('ocr_confidence', 1.0)
                }
            })

        return {
            'document_id': os.path.basename(file_path),
            'slides': processed_data
        }

def main():
    # Example usage
    upload_dir = "data/input"
    output_dir = "data/processed"
    
    pipeline = DocumentIngestionPipeline(upload_dir, output_dir)
    
    # Process all files in upload directory
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        try:
            result = pipeline.process_document(file_path)
            print(f"Successfully processed {filename}")
            print(f"Found {len(result['slides'])} slides")
            
            # Print some statistics
            total_text = sum(len(slide['content']) for slide in result['slides'])
            total_images = sum(len(slide['images']) for slide in result['slides'])
            print(f"Total text characters: {total_text}")
            print(f"Total images: {total_images}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main() 