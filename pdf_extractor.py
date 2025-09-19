"""
PDF Text Extraction Module
Handles extraction of text from PDF files using multiple methods for better accuracy.
"""

import pdfplumber
import PyPDF2
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract text from PDF files using multiple extraction methods."""
    
    def __init__(self):
        self.extraction_methods = ['pdfplumber', 'PyPDF2']
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF file using the best available method.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If extraction fails
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            text = self._extract_with_pdfplumber(pdf_path)
            if text and len(text.strip()) > 100:  # Minimum content check
                logger.info(f"Successfully extracted text using pdfplumber from {pdf_path}")
                return text
            
            # Fallback to PyPDF2
            text = self._extract_with_pypdf2(pdf_path)
            if text and len(text.strip()) > 100:
                logger.info(f"Successfully extracted text using PyPDF2 from {pdf_path}")
                return text
            
            raise Exception("Failed to extract meaningful text from PDF")
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            raise
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber library."""
        try:
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(page_text)
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
                        continue
            
            return '\n\n'.join(text_content)
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
            return ""
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2 library."""
        try:
            text_content = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(page_text)
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
                        continue
            
            return '\n\n'.join(text_content)
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {str(e)}")
            return ""
    
    def get_page_count(self, pdf_path: str) -> int:
        """Get the number of pages in the PDF."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        except Exception:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    return len(pdf_reader.pages)
            except Exception:
                return 0
