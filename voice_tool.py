"""
Voice Tool - Text-to-Speech Generation
Handles voice generation from text using VBee TTS API.
"""

import os
import logging
from typing import Dict, Optional, List
from voice_generator import VoiceGenerator

logger = logging.getLogger(__name__)


class VoiceTool:
    """Tool for generating voice audio from text using VBee TTS API."""
    
    def __init__(self, vbee_token: str = None, vbee_app_id: str = None):
        """
        Initialize the voice tool.
        
        Args:
            vbee_token (str): VBee API token (optional, can use environment variable)
            vbee_app_id (str): VBee app ID (optional, can use environment variable)
        """
        self.voice_generator = VoiceGenerator(token=vbee_token, app_id=vbee_app_id)
    
    def generate_voice_from_file(self, summary_file_path: str, output_dir: str = None, 
                                voice_code: str = "", speed_rate: str = "1.0", 
                                callback_url: str = "") -> Dict[str, any]:
        """
        Generate voice from a summary text file.
        
        Args:
            summary_file_path (str): Path to the summary text file
            output_dir (str): Directory to save audio files (optional)
            voice_code (str): Voice code for TTS (optional)
            speed_rate (str): Speech speed rate (default: 1.0)
            callback_url (str): Callback URL for async processing (optional)
            
        Returns:
            Dict containing generation results and file paths
        """
        try:
            logger.info(f"Generating voice from summary file: {summary_file_path}")
            
            result = self.voice_generator.generate_voice_from_file(
                summary_file_path=summary_file_path,
                output_dir=output_dir,
                voice_code=voice_code,
                speed_rate=speed_rate,
                callback_url=callback_url
            )
            
            logger.info("Voice generation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error generating voice from file: {str(e)}")
            raise
    
    def generate_voice_from_text(self, text: str, output_dir: str = None,
                                voice_code: str = "", speed_rate: str = "1.0",
                                callback_url: str = "") -> Dict[str, any]:
        """
        Generate voice directly from text.
        
        Args:
            text (str): Text to convert to speech
            output_dir (str): Directory to save audio files (optional)
            voice_code (str): Voice code for TTS (optional)
            speed_rate (str): Speech speed rate (default: 1.0)
            callback_url (str): Callback URL for async processing (optional)
            
        Returns:
            Dict containing generation results
        """
        try:
            logger.info(f"Generating voice from text ({len(text)} characters)")
            
            result = self.voice_generator.generate_voice_from_text(
                text=text,
                output_dir=output_dir,
                voice_code=voice_code,
                speed_rate=speed_rate,
                callback_url=callback_url
            )
            
            logger.info("Voice generation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error generating voice from text: {str(e)}")
            raise
    
    def generate_voice_from_summary_result(self, summary_result: dict, output_dir: str = None,
                                         voice_code: str = "", speed_rate: str = "1.0",
                                         callback_url: str = "") -> Dict[str, any]:
        """
        Generate voice from a summary result dictionary.
        
        Args:
            summary_result (dict): Summary result from SummaryTool
            output_dir (str): Directory to save audio files (optional)
            voice_code (str): Voice code for TTS (optional)
            speed_rate (str): Speech speed rate (default: 1.0)
            callback_url (str): Callback URL for async processing (optional)
            
        Returns:
            Dict containing generation results
        """
        try:
            # Extract summary text from the result
            summary_text = summary_result.get('summary', '')
            if not summary_text:
                raise ValueError("No summary text found in summary result")
            
            logger.info(f"Generating voice from summary result ({len(summary_text)} characters)")
            
            result = self.voice_generator.generate_voice_from_text(
                text=summary_text,
                output_dir=output_dir,
                voice_code=voice_code,
                speed_rate=speed_rate,
                callback_url=callback_url
            )
            
            # Add summary metadata to result
            result['summary_metadata'] = {
                'original_words': summary_result.get('original_word_count', 0),
                'summary_words': summary_result.get('word_count', 0),
                'estimated_duration': summary_result.get('estimated_duration_minutes', 0),
                'source': summary_result.get('pdf_path', 'Text Input')
            }
            
            logger.info("Voice generation from summary result completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error generating voice from summary result: {str(e)}")
            raise
    
    def set_vbee_credentials(self, token: str, app_id: str):
        """Update VBee credentials."""
        self.voice_generator.set_credentials(token, app_id)
    
    def get_voice_stats(self, voice_result: dict) -> dict:
        """Get statistics about the voice generation."""
        return {
            'audio_files_count': len(voice_result.get('audio_files', [])),
            'total_sections': voice_result.get('total_sections', 0),
            'total_chunks': voice_result.get('total_chunks', 0),
            'output_directory': voice_result.get('output_directory', ''),
            'success': voice_result.get('success', False),
            'error': voice_result.get('error', None)
        }
    
    def list_audio_files(self, voice_result: dict) -> List[str]:
        """Get list of generated audio files."""
        return voice_result.get('audio_files', [])
    
    def estimate_voice_duration(self, text_length: int, speed_rate: float = 1.0) -> float:
        """
        Estimate voice duration based on text length and speed rate.
        
        Args:
            text_length (int): Length of text in characters
            speed_rate (float): Speech speed rate
            
        Returns:
            float: Estimated duration in minutes
        """
        # Rough estimation: ~150 characters per minute at normal speed
        base_chars_per_minute = 150
        adjusted_chars_per_minute = base_chars_per_minute * speed_rate
        estimated_minutes = text_length / adjusted_chars_per_minute
        return round(estimated_minutes, 2)
    
    def validate_voice_settings(self, voice_code: str, speed_rate: str) -> dict:
        """
        Validate voice generation settings.
        
        Args:
            voice_code (str): Voice code to validate
            speed_rate (str): Speed rate to validate
            
        Returns:
            dict: Validation results
        """
        validation = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Validate speed rate
        try:
            speed = float(speed_rate)
            if speed < 0.5:
                validation['warnings'].append("Speed rate is very slow (< 0.5)")
            elif speed > 2.0:
                validation['warnings'].append("Speed rate is very fast (> 2.0)")
        except ValueError:
            validation['errors'].append("Invalid speed rate format")
            validation['valid'] = False
        
        # Validate voice code (basic check)
        if voice_code and len(voice_code) > 50:
            validation['warnings'].append("Voice code seems unusually long")
        
        return validation
