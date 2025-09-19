"""
Configuration settings for PDF Text Summarizer
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "PDF Text Summarizer"
APP_VERSION = "1.0.0"

# Default settings
DEFAULT_VIDEO_DURATION_MINUTES = 15
DEFAULT_WORDS_PER_MINUTE = 155  # Average speaking rate
DEFAULT_OUTPUT_DIR = "summaries"

# Text processing settings
MIN_TEXT_LENGTH = 100  # Minimum characters for meaningful text
MAX_SUMMARY_SENTENCES = 10
MAX_KEY_POINTS = 5
MAX_KEY_TOPICS = 10

# File settings
SUPPORTED_EXTENSIONS = ['.pdf']
MAX_FILE_SIZE_MB = 50  # Maximum file size in MB

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'pdf_summarizer.log'

# OpenAI settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 1000
OPENAI_TEMPERATURE = 0.3
OPENAI_TOP_P = 0.9
MAX_CHUNK_LENGTH = 12000  # Conservative limit for GPT-3.5-turbo

# Traditional model settings (fallback)
MAX_MODEL_LENGTH = 1024
MIN_SUMMARY_LENGTH = 50
MAX_SUMMARY_LENGTH = 150

# Reading metrics thresholds
READABILITY_THRESHOLDS = {
    'flesch_reading_ease': {
        'very_easy': 90,
        'easy': 80,
        'fairly_easy': 70,
        'standard': 60,
        'fairly_difficult': 50,
        'difficult': 30,
        'very_difficult': 0
    }
}

# Error messages
ERROR_MESSAGES = {
    'file_not_found': "PDF file not found: {file_path}",
    'invalid_file_type': "File must be a PDF document (.pdf extension)",
    'file_too_large': "File size exceeds maximum allowed size of {max_size}MB",
    'insufficient_text': "Insufficient text extracted from PDF (minimum {min_length} characters required)",
    'extraction_failed': "Failed to extract text from PDF",
    'summarization_failed': "Failed to create summary",
    'save_failed': "Failed to save summary to file",
    'openai_api_key_missing': "OpenAI API key not found. Please set OPENAI_API_KEY environment variable or use --api-key option",
    'openai_api_error': "OpenAI API error: {error_message}",
    'openai_rate_limit': "OpenAI rate limit exceeded. Please try again later",
    'openai_quota_exceeded': "OpenAI quota exceeded. Please check your billing"
}

# Success messages
SUCCESS_MESSAGES = {
    'processing_complete': "PDF processing completed successfully",
    'summary_saved': "Summary saved to: {output_path}",
    'text_extracted': "Successfully extracted {word_count} words from PDF"
}
