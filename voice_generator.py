"""
Voice Generation Module using VBee TTS API
Converts text summaries to audio files for video creation.
"""

import json
import os
import time
import logging
from typing import Dict, Optional, List
import requests
from pathlib import Path

logger = logging.getLogger(__name__)


class VoiceGenerator:
    """Generate voice audio from text using VBee TTS API."""
    
    def __init__(self, token: str = None, app_id: str = None):
        """
        Initialize voice generator with VBee TTS credentials.
        
        Args:
            token (str): VBee API token
            app_id (str): VBee application ID
        """
        self.token = token or os.getenv('VBEE_TOKEN')
        self.app_id = app_id or os.getenv('VBEE_APP_ID')
        self.base_url = "https://vbee.vn/api/v1/tts"
        self.timeout = 120  # 2 minutes timeout
        
        if not self.token:
            raise ValueError("VBee token is required. Set VBEE_TOKEN environment variable or pass token parameter.")
        if not self.app_id:
            raise ValueError("VBee app ID is required. Set VBEE_APP_ID environment variable or pass app_id parameter.")
    
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
            # Read the summary file
            summary_text = self._read_summary_file(summary_file_path)
            
            # Extract text sections
            sections = self._extract_text_sections(summary_text)
            
            # Generate voice for each section
            audio_files = []
            for i, section in enumerate(sections):
                logger.info(f"Generating voice for section {i+1}/{len(sections)}")
                audio_file = self._generate_section_voice(
                    section, i+1, output_dir, voice_code, speed_rate, callback_url
                )
                if audio_file:
                    audio_files.append(audio_file)
            
            return {
                'success': True,
                'audio_files': audio_files,
                'total_sections': len(sections),
                'summary_file': summary_file_path,
                'output_directory': output_dir or os.path.dirname(summary_file_path)
            }
            
        except Exception as e:
            logger.error(f"Error generating voice: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'audio_files': [],
                'total_sections': 0
            }
    
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
            # Split text into manageable chunks
            chunks = self._split_text_into_chunks(text, max_length=1000)
            
            audio_files = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Generating voice for chunk {i+1}/{len(chunks)}")
                audio_file = self._generate_chunk_voice(
                    chunk, i+1, output_dir, voice_code, speed_rate, callback_url
                )
                if audio_file:
                    audio_files.append(audio_file)
            
            return {
                'success': True,
                'audio_files': audio_files,
                'total_chunks': len(chunks),
                'output_directory': output_dir or '.'
            }
            
        except Exception as e:
            logger.error(f"Error generating voice: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'audio_files': [],
                'total_chunks': 0
            }
    
    def _read_summary_file(self, file_path: str) -> str:
        """Read and parse summary file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the main summary section
            summary_start = content.find("SUMMARY")
            if summary_start != -1:
                summary_section = content[summary_start:]
                # Find the end of summary (next section or end of file)
                next_section = summary_section.find("\n\nKEY POINTS")
                if next_section != -1:
                    summary_text = summary_section[:next_section]
                else:
                    summary_text = summary_section
                
                # Clean up the summary text
                summary_text = summary_text.replace("SUMMARY\n", "").replace("-" * 20, "").strip()
                return summary_text
            
            # If no SUMMARY section found, return the whole content
            return content
            
        except Exception as e:
            logger.error(f"Error reading summary file: {str(e)}")
            raise
    
    def _extract_text_sections(self, text: str) -> List[str]:
        """Extract logical sections from the summary text."""
        # Split by paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Combine small paragraphs
        sections = []
        current_section = ""
        
        for paragraph in paragraphs:
            if len(current_section + paragraph) < 800:  # Keep sections under 800 chars
                current_section += paragraph + " "
            else:
                if current_section:
                    sections.append(current_section.strip())
                current_section = paragraph + " "
        
        if current_section:
            sections.append(current_section.strip())
        
        return sections
    
    def _split_text_into_chunks(self, text: str, max_length: int = 1000) -> List[str]:
        """Split text into chunks suitable for TTS."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_length and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _generate_section_voice(self, text: str, section_num: int, output_dir: str,
                               voice_code: str, speed_rate: str, callback_url: str) -> Optional[str]:
        """Generate voice for a single section."""
        try:
            # Create output filename
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"section_{section_num:02d}.mp3")
            else:
                output_file = f"section_{section_num:02d}.mp3"
            
            # Call VBee TTS API
            response = self._call_vbee_api(text, voice_code, speed_rate, callback_url)
            
            if response and 'audio_url' in response:
                # Download the audio file
                audio_url = response['audio_url']
                self._download_audio_file(audio_url, output_file)
                logger.info(f"Generated audio file: {output_file}")
                return output_file
            else:
                logger.error(f"Failed to generate voice for section {section_num}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating voice for section {section_num}: {str(e)}")
            return None
    
    def _generate_chunk_voice(self, text: str, chunk_num: int, output_dir: str,
                             voice_code: str, speed_rate: str, callback_url: str) -> Optional[str]:
        """Generate voice for a single chunk."""
        try:
            # Create output filename
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"chunk_{chunk_num:02d}.mp3")
            else:
                output_file = f"chunk_{chunk_num:02d}.mp3"
            
            # Call VBee TTS API
            response = self._call_vbee_api(text, voice_code, speed_rate, callback_url)
            
            if response and 'audio_url' in response:
                # Download the audio file
                audio_url = response['audio_url']
                self._download_audio_file(audio_url, output_file)
                logger.info(f"Generated audio file: {output_file}")
                return output_file
            else:
                logger.error(f"Failed to generate voice for chunk {chunk_num}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating voice for chunk {chunk_num}: {str(e)}")
            return None
    
    def _call_vbee_api(self, text: str, voice_code: str, speed_rate: str, callback_url: str) -> Optional[Dict]:
        """Call VBee TTS API."""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
            
            payload = {
                "voice_code": voice_code,
                "speed_rate": speed_rate,
                "input_text": text,
                "app_id": self.app_id,
                "callback_url": callback_url
            }
            
            logger.info(f"Calling VBee TTS API for text length: {len(text)} characters")
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("VBee TTS API call successful")
                return result
            else:
                logger.error(f"VBee TTS API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("VBee TTS API timeout")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"VBee TTS API request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling VBee TTS API: {str(e)}")
            return None
    
    def _download_audio_file(self, audio_url: str, output_file: str):
        """Download audio file from URL."""
        try:
            response = requests.get(audio_url, timeout=60)
            response.raise_for_status()
            
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded audio file: {output_file}")
            
        except Exception as e:
            logger.error(f"Error downloading audio file: {str(e)}")
            raise
    
    def set_credentials(self, token: str, app_id: str):
        """Update VBee credentials."""
        self.token = token
        self.app_id = app_id
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices (if API supports it)."""
        # This would need to be implemented based on VBee API documentation
        # For now, return empty list
        return []
    
    def estimate_cost(self, text_length: int) -> Dict[str, any]:
        """Estimate cost for voice generation."""
        # This would need to be implemented based on VBee pricing
        # For now, return placeholder
        return {
            'estimated_cost': 'Contact VBee for pricing',
            'text_length': text_length,
            'note': 'Pricing depends on voice type and length'
        }
