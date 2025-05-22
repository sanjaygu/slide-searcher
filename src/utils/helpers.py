import logging
import os
from typing import List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories(base_path: str) -> None:
    """
    Create necessary directories if they don't exist.
    """
    directories = [
        os.path.join(base_path, "data", "uploads"),
        os.path.join(base_path, "data", "rendered_images"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_file_extension(filename: str) -> str:
    """
    Get file extension in lowercase.
    """
    return os.path.splitext(filename)[1].lower()

def is_valid_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Check if file type is allowed.
    """
    return get_file_extension(filename) in allowed_extensions

def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename using timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}{ext}"

def cleanup_old_files(directory: str, max_age_days: int = 7) -> None:
    """
    Clean up files older than max_age_days.
    """
    current_time = datetime.now()
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            age_days = (current_time - file_time).days
            
            if age_days > max_age_days:
                try:
                    os.remove(filepath)
                    logger.info(f"Removed old file: {filepath}")
                except Exception as e:
                    logger.error(f"Error removing file {filepath}: {str(e)}") 