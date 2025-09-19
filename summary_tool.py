"""
Summary Tool - PDF Text Summarization
Handles PDF text extraction and summarization using OpenAI.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from pdf_extractor import PDFExtractor
from text_summarizer import TextSummarizer

logger = logging.getLogger(__name__)


class SummaryTool:
    """Tool for PDF text extraction and summarization."""
    
    def __init__(self, openai_api_key: str = None):
        """
        Initialize the summary tool.
        
        Args:
            openai_api_key (str): OpenAI API key (optional, can use environment variable)
        """
        self.pdf_extractor = PDFExtractor()
        self.text_summarizer = TextSummarizer(api_key=openai_api_key)
    
    def process_pdf(self, pdf_path: str, output_path: str = None, duration_minutes: int = 15) -> dict:
        """
        Process a PDF file and create a video-ready summary.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_path (str): Path to save the summary (optional)
            duration_minutes (int): Target video duration in minutes
            
        Returns:
            dict: Summary results
        """
        try:
            # Validate input file
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            if not pdf_path.lower().endswith('.pdf'):
                raise ValueError("File must be a PDF document")
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Extract text from PDF
            logger.info("Extracting text from PDF...")
            extracted_text = self.pdf_extractor.extract_text(pdf_path)
            
            if not extracted_text or len(extracted_text.strip()) < 100:
                raise ValueError("Insufficient text extracted from PDF")
            
            logger.info(f"Extracted {len(extracted_text.split())} words from PDF")
            
            # Get PDF metadata
            page_count = self.pdf_extractor.get_page_count(pdf_path)
            
            # Create summary
            logger.info("Creating summary...")
            summary_result = self.text_summarizer.summarize_for_video(
                extracted_text, 
                duration_minutes
            )
            
            # Add metadata
            summary_result['pdf_path'] = pdf_path
            summary_result['pdf_page_count'] = page_count
            summary_result['processed_at'] = datetime.now().isoformat()
            
            # Save to file if output path provided
            if output_path:
                self._save_summary(summary_result, output_path)
            
            logger.info("PDF processing completed successfully")
            return summary_result
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
    
    def summarize_text(self, text: str, duration_minutes: int = 15, output_path: str = None) -> dict:
        """
        Summarize text content directly.
        
        Args:
            text (str): Text content to summarize
            duration_minutes (int): Target video duration in minutes
            output_path (str): Path to save the summary (optional)
            
        Returns:
            dict: Summary results
        """
        try:
            logger.info(f"Summarizing text ({len(text.split())} words)")
            
            # Create summary
            summary_result = self.text_summarizer.summarize_for_video(text, duration_minutes)
            
            # Add metadata
            summary_result['processed_at'] = datetime.now().isoformat()
            summary_result['input_type'] = 'text'
            
            # Save to file if output path provided
            if output_path:
                self._save_summary(summary_result, output_path)
            
            logger.info("Text summarization completed successfully")
            return summary_result
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            raise
    
    def _save_summary(self, summary_result: dict, output_path: str):
        """Save summary result to file."""
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save as text file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("PDF TEXT SUMMARIZER - VIDEO READY SUMMARY\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Source: {summary_result.get('pdf_path', 'Text Input')}\n")
                f.write(f"Pages: {summary_result.get('pdf_page_count', 'N/A')}\n")
                f.write(f"Original Word Count: {summary_result['original_word_count']}\n")
                f.write(f"Summary Word Count: {summary_result['word_count']}\n")
                f.write(f"Target Duration: {summary_result['estimated_duration_minutes']} minutes\n")
                f.write(f"Processed: {summary_result['processed_at']}\n\n")
                
                f.write("SUMMARY\n")
                f.write("-" * 20 + "\n")
                f.write(summary_result['summary'] + "\n\n")
                
                f.write("KEY POINTS\n")
                f.write("-" * 20 + "\n")
                for i, point in enumerate(summary_result['key_points'], 1):
                    f.write(f"{i}. {point}\n")
                f.write("\n")
                
                f.write("KEY TOPICS\n")
                f.write("-" * 20 + "\n")
                for topic, count in summary_result['key_topics']:
                    f.write(f"• {topic} (mentioned {count} times)\n")
                f.write("\n")
                
                if summary_result['reading_metrics']:
                    f.write("READING METRICS\n")
                    f.write("-" * 20 + "\n")
                    for metric, value in summary_result['reading_metrics'].items():
                        f.write(f"• {metric.replace('_', ' ').title()}: {value:.2f}\n")
            
            logger.info(f"Summary saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving summary: {str(e)}")
            raise
    
    def set_openai_api_key(self, api_key: str):
        """Set OpenAI API key."""
        self.text_summarizer.set_api_key(api_key)
    
    def is_openai_available(self) -> bool:
        """Check if OpenAI API is available."""
        return self.text_summarizer.is_openai_available()
    
    def get_summary_stats(self, summary_result: dict) -> dict:
        """Get statistics about the summary."""
        return {
            'original_words': summary_result['original_word_count'],
            'summary_words': summary_result['word_count'],
            'compression_ratio': round(summary_result['original_word_count'] / summary_result['word_count'], 2),
            'estimated_duration': summary_result['estimated_duration_minutes'],
            'key_points_count': len(summary_result['key_points']),
            'key_topics_count': len(summary_result['key_topics']),
            'summarization_method': summary_result.get('summarization_method', 'openai')
        }
