"""
Text Summarization Module using OpenAI API
Optimized for creating summaries suitable for 15-minute video content.
"""

import re
import nltk
import os
from typing import List, Dict, Tuple
from openai import OpenAI
import textstat
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TextSummarizer:
    """Summarize text content using OpenAI API, optimized for 15-minute video format."""
    
    def __init__(self, api_key: str = None):
        self._download_nltk_data()
        self._initialize_openai_client(api_key)
    
    def _download_nltk_data(self):
        """Download required NLTK data."""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {str(e)}")
    
    def _initialize_openai_client(self, api_key: str = None):
        """Initialize OpenAI client."""
        try:
            # Get API key from parameter, environment variable, or .env file
            if api_key:
                self.api_key = api_key
            else:
                self.api_key = os.getenv('OPENAI_API_KEY')
            
            if not self.api_key:
                raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable or pass api_key parameter.")
            
            self.openai_client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise
    
    def summarize_for_video(self, text: str, target_duration_minutes: int = 15) -> Dict[str, any]:
        """
        Create a summary optimized for video content of specified duration using OpenAI.
        
        Args:
            text (str): Input text to summarize
            target_duration_minutes (int): Target video duration in minutes
            
        Returns:
            Dict containing summary, key points, and metadata
        """
        try:
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Calculate target word count based on speaking rate
            target_word_count = self._calculate_target_word_count(target_duration_minutes)
            
            # Extract key sections and topics
            sections = self._extract_sections(cleaned_text)
            key_topics = self._extract_key_topics(cleaned_text)
            
            # Create summary using OpenAI
            summary = self._create_openai_summary(cleaned_text, target_word_count, target_duration_minutes)
            
            if not summary:
                raise ValueError("Failed to generate summary using OpenAI")
            
            # Extract key points for visual presentation
            key_points = self._extract_key_points(cleaned_text, summary)
            
            # Calculate reading metrics
            reading_metrics = self._calculate_reading_metrics(summary)
            
            return {
                'summary': summary,
                'key_points': key_points,
                'key_topics': key_topics,
                'sections': sections,
                'word_count': len(summary.split()),
                'target_word_count': target_word_count,
                'estimated_duration_minutes': self._estimate_reading_time(summary),
                'reading_metrics': reading_metrics,
                'original_word_count': len(text.split()),
                'summarization_method': 'openai'
            }
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\']', '', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'\b\d+\b(?=\s*$)', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def _calculate_target_word_count(self, duration_minutes: int) -> int:
        """Calculate target word count based on speaking rate."""
        # Average speaking rate: 150-160 words per minute
        # Use 155 words per minute as baseline
        words_per_minute = 155
        return duration_minutes * words_per_minute
    
    def _extract_sections(self, text: str) -> List[Dict[str, str]]:
        """Extract main sections from the text."""
        sections = []
        
        # Split by common section markers
        section_patterns = [
            r'\n\s*\d+\.\s+[A-Z][^.\n]*',  # Numbered sections
            r'\n\s*[A-Z][A-Z\s]+:',  # ALL CAPS headers
            r'\n\s*[A-Z][^.\n]*\n(?=[A-Z])',  # Title case headers
        ]
        
        for pattern in section_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                sections.append({
                    'title': match.group().strip(),
                    'position': match.start()
                })
        
        return sections[:10]  # Limit to top 10 sections
    
    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from the text."""
        # Simple keyword extraction based on frequency and importance
        words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other', 'after', 'first', 'well', 'also', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
        
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top 10 most frequent words
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _create_openai_summary(self, text: str, target_word_count: int, duration_minutes: int) -> str:
        """Create summary using OpenAI API."""
        try:
            # Split text into chunks if too long (OpenAI has token limits)
            max_chunk_length = 12000  # Conservative limit for GPT-3.5-turbo
            chunks = self._split_text_into_chunks(text, max_chunk_length)
            
            summaries = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)} with OpenAI")
                
                # Create prompt for video-optimized summary
                prompt = self._create_summary_prompt(chunk, target_word_count, duration_minutes)
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert content creator who specializes in creating video-ready summaries. Your summaries are engaging, clear, and optimized for spoken presentation."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=min(1000, target_word_count * 1.5),  # Allow some flexibility
                    temperature=0.3,  # Lower temperature for more consistent summaries
                    top_p=0.9
                )
                
                chunk_summary = response.choices[0].message.content.strip()
                summaries.append(chunk_summary)
            
            # Combine summaries
            combined_summary = ' '.join(summaries)
            
            # If combined summary is too long, ask OpenAI to shorten it
            if len(combined_summary.split()) > target_word_count * 1.2:
                logger.info("Summary too long, requesting shorter version from OpenAI")
                shorten_prompt = f"""Please shorten this summary to approximately {target_word_count} words while maintaining all key information and making it suitable for a {duration_minutes}-minute video presentation:

{combined_summary}"""
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert at creating concise, video-ready summaries."},
                        {"role": "user", "content": shorten_prompt}
                    ],
                    max_tokens=target_word_count + 200,
                    temperature=0.3
                )
                
                combined_summary = response.choices[0].message.content.strip()
            
            return combined_summary
            
        except Exception as e:
            logger.error(f"OpenAI summarization failed: {str(e)}")
            raise
    
    def _create_summary_prompt(self, text: str, target_word_count: int, duration_minutes: int) -> str:
        """Create a prompt for OpenAI summarization."""
        return f"""Please create a comprehensive summary of the following text that is optimized for a {duration_minutes}-minute video presentation. The summary should be approximately {target_word_count} words and should:

1. Capture all main concepts and key findings
2. Be engaging and suitable for spoken presentation
3. Include important details while remaining concise
4. Flow naturally for video narration
5. Highlight the most significant points

Text to summarize:
{text}

Please provide a well-structured summary that would work perfectly for a {duration_minutes}-minute video script."""
    
    def _split_text_into_chunks(self, text: str, max_length: int) -> List[str]:
        """Split text into chunks that fit within token limits."""
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
    
    def _extract_key_points(self, original_text: str, summary: str) -> List[str]:
        """Extract key points for visual presentation."""
        # Extract sentences that contain important information
        sentences = re.split(r'[.!?]+', summary)
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 100:  # Good length for key points
                # Check if sentence contains important keywords
                important_words = ['important', 'key', 'main', 'primary', 'essential', 'critical', 'significant', 'major', 'core', 'fundamental']
                if any(word in sentence.lower() for word in important_words):
                    key_points.append(sentence)
                elif len(key_points) < 5:  # Limit to 5 key points
                    key_points.append(sentence)
        
        return key_points[:5]
    
    def _calculate_reading_metrics(self, text: str) -> Dict[str, float]:
        """Calculate reading difficulty metrics."""
        try:
            return {
                'flesch_reading_ease': textstat.flesch_reading_ease(text),
                'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
                'automated_readability_index': textstat.automated_readability_index(text),
                'coleman_liau_index': textstat.coleman_liau_index(text)
            }
        except Exception:
            return {}
    
    def _estimate_reading_time(self, text: str) -> float:
        """Estimate reading time in minutes."""
        word_count = len(text.split())
        words_per_minute = 155  # Average speaking rate
        return round(word_count / words_per_minute, 1)
    
    def set_api_key(self, api_key: str):
        """Set OpenAI API key and reinitialize client."""
        self.api_key = api_key
        self._initialize_openai_client(api_key)
    
    def is_openai_available(self) -> bool:
        """Check if OpenAI API is available."""
        return self.openai_client is not None