"""
Utility functions for PDF Text Summarizer
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def validate_pdf_file(file_path: str) -> Dict[str, Any]:
    """
    Validate PDF file before processing.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        Dict containing validation results
    """
    validation_result = {
        'is_valid': False,
        'errors': [],
        'warnings': [],
        'file_info': {}
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            validation_result['errors'].append(f"File not found: {file_path}")
            return validation_result
        
        # Check file extension
        if not file_path.lower().endswith('.pdf'):
            validation_result['errors'].append("File must have .pdf extension")
            return validation_result
        
        # Get file info
        file_stat = os.stat(file_path)
        file_size_mb = file_stat.st_size / (1024 * 1024)
        
        validation_result['file_info'] = {
            'size_mb': round(file_size_mb, 2),
            'size_bytes': file_stat.st_size,
            'path': file_path,
            'name': Path(file_path).name
        }
        
        # Check file size
        from config import MAX_FILE_SIZE_MB
        if file_size_mb > MAX_FILE_SIZE_MB:
            validation_result['errors'].append(
                f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB}MB)"
            )
            return validation_result
        
        # Check if file is readable
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if header != b'%PDF':
                    validation_result['errors'].append("File does not appear to be a valid PDF")
                    return validation_result
        except Exception as e:
            validation_result['errors'].append(f"Cannot read file: {str(e)}")
            return validation_result
        
        validation_result['is_valid'] = True
        
        # Add warnings for large files
        if file_size_mb > 10:
            validation_result['warnings'].append(f"Large file ({file_size_mb:.2f}MB) may take longer to process")
        
    except Exception as e:
        validation_result['errors'].append(f"Validation error: {str(e)}")
    
    return validation_result


def clean_filename(filename: str) -> str:
    """
    Clean filename for safe file operations.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Cleaned filename
    """
    # Remove or replace invalid characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove extra spaces and dots
    cleaned = re.sub(r'\s+', '_', cleaned)
    cleaned = cleaned.strip('._')
    
    # Ensure it's not empty
    if not cleaned:
        cleaned = 'unnamed_file'
    
    return cleaned


def format_duration(minutes: float) -> str:
    """
    Format duration in a human-readable format.
    
    Args:
        minutes (float): Duration in minutes
        
    Returns:
        str: Formatted duration string
    """
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} seconds"
    elif minutes < 60:
        return f"{minutes:.1f} minutes"
    else:
        hours = int(minutes // 60)
        remaining_minutes = minutes % 60
        if remaining_minutes > 0:
            return f"{hours}h {remaining_minutes:.1f}m"
        else:
            return f"{hours} hours"


def format_word_count(word_count: int) -> str:
    """
    Format word count in a human-readable format.
    
    Args:
        word_count (int): Number of words
        
    Returns:
        str: Formatted word count string
    """
    if word_count < 1000:
        return f"{word_count} words"
    elif word_count < 1000000:
        return f"{word_count/1000:.1f}K words"
    else:
        return f"{word_count/1000000:.1f}M words"


def create_output_filename(pdf_path: str, duration_minutes: int = 15) -> str:
    """
    Create output filename based on PDF path and duration.
    
    Args:
        pdf_path (str): Path to the PDF file
        duration_minutes (int): Target duration in minutes
        
    Returns:
        str: Generated output filename
    """
    pdf_name = Path(pdf_path).stem
    cleaned_name = clean_filename(pdf_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{cleaned_name}_summary_{duration_minutes}min_{timestamp}.txt"


def ensure_output_directory(output_path: str) -> None:
    """
    Ensure output directory exists.
    
    Args:
        output_path (str): Path to the output file
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in MB.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to specified length.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add when truncating
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def extract_metadata_from_text(text: str) -> Dict[str, Any]:
    """
    Extract metadata from text content.
    
    Args:
        text (str): Text content
        
    Returns:
        Dict containing extracted metadata
    """
    metadata = {
        'word_count': len(text.split()),
        'character_count': len(text),
        'sentence_count': len(re.split(r'[.!?]+', text)),
        'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
        'has_numbers': bool(re.search(r'\d', text)),
        'has_urls': bool(re.search(r'http[s]?://', text)),
        'has_emails': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    }
    
    return metadata


# Import datetime for create_output_filename function
from datetime import datetime
