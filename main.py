"""
PDF Text Summarizer - Main Application
A Python application to summarize PDF files into text suitable for 15-minute video content.
"""

import click
import logging
import os
import sys
from pathlib import Path
from summary_tool import SummaryTool
from voice_tool import VoiceTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_summarizer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class PDFSummarizerApp:
    """Main application class for PDF text summarization and voice generation."""
    
    def __init__(self):
        self.summary_tool = None
        self.voice_tool = None
    
    def initialize_summary_tool(self, openai_api_key: str = None):
        """Initialize the summary tool."""
        self.summary_tool = SummaryTool(openai_api_key=openai_api_key)
    
    def initialize_voice_tool(self, vbee_token: str = None, vbee_app_id: str = None):
        """Initialize the voice tool."""
        self.voice_tool = VoiceTool(vbee_token=vbee_token, vbee_app_id=vbee_app_id)


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path for the summary')
@click.option('--duration', '-d', default=15, help='Target video duration in minutes (default: 15)')
@click.option('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
@click.option('--generate-voice', is_flag=True, help='Generate voice audio from summary')
@click.option('--voice-output-dir', type=click.Path(), help='Directory for voice audio files')
@click.option('--voice-code', default='', help='Voice code for TTS (optional)')
@click.option('--speed-rate', default='1.0', help='Speech speed rate (default: 1.0)')
@click.option('--callback-url', default='', help='Callback URL for async voice processing (optional)')
@click.option('--vbee-token', help='VBee API token (or set VBEE_TOKEN environment variable)')
@click.option('--vbee-app-id', help='VBee app ID (or set VBEE_APP_ID environment variable)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(pdf_path, output, duration, api_key, generate_voice, voice_output_dir, voice_code, 
         speed_rate, callback_url, vbee_token, vbee_app_id, verbose):
    """
    PDF Text Summarizer - Convert PDF content to video-ready text summary.
    
    PDF_PATH: Path to the PDF file to summarize
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize application
        app = PDFSummarizerApp()
        
        # Initialize summary tool
        app.initialize_summary_tool(openai_api_key=api_key)
        
        # Check OpenAI availability
        if not app.summary_tool.is_openai_available():
            click.echo("Error: OpenAI API key is required.")
            click.echo("Please set OPENAI_API_KEY environment variable or use --api-key option")
            click.echo("Get your API key from: https://platform.openai.com/api-keys")
            sys.exit(1)
        
        # Initialize voice tool if voice generation is requested
        if generate_voice:
            app.initialize_voice_tool(vbee_token=vbee_token, vbee_app_id=vbee_app_id)
            click.echo("Voice generation enabled")
        
        # Generate output path if not provided
        if not output:
            pdf_name = Path(pdf_path).stem
            output = f"{pdf_name}_summary_{duration}min.txt"
        
        # Process PDF
        click.echo(f"Processing PDF: {pdf_path}")
        click.echo(f"Target duration: {duration} minutes")
        click.echo("Extracting text and creating summary...")
        
        result = app.summary_tool.process_pdf(pdf_path, output, duration)
        
        # Display results
        click.echo("\n" + "="*60)
        click.echo("SUMMARY COMPLETED SUCCESSFULLY!")
        click.echo("="*60)
        click.echo(f"Source PDF: {result['pdf_path']}")
        click.echo(f"Pages processed: {result['pdf_page_count']}")
        click.echo(f"Original words: {result['original_word_count']}")
        click.echo(f"Summary words: {result['word_count']}")
        click.echo(f"Estimated duration: {result['estimated_duration_minutes']} minutes")
        click.echo(f"Summarization method: {result.get('summarization_method', 'openai').upper()}")
        click.echo(f"Summary saved to: {output}")
        
        click.echo("\nSUMMARY PREVIEW:")
        click.echo("-" * 40)
        preview = result['summary'][:500] + "..." if len(result['summary']) > 500 else result['summary']
        click.echo(preview)
        
        click.echo("\nKEY POINTS:")
        click.echo("-" * 40)
        for i, point in enumerate(result['key_points'], 1):
            click.echo(f"{i}. {point}")
        
        # Generate voice if requested
        if generate_voice:
            click.echo("\n" + "="*60)
            click.echo("GENERATING VOICE AUDIO...")
            click.echo("="*60)
            
            try:
                voice_result = app.voice_tool.generate_voice_from_summary_result(
                    summary_result=result,
                    output_dir=voice_output_dir,
                    voice_code=voice_code,
                    speed_rate=speed_rate,
                    callback_url=callback_url
                )
                
                if voice_result['success']:
                    click.echo("✓ Voice generation completed successfully!")
                    click.echo(f"Audio files generated: {len(voice_result['audio_files'])}")
                    click.echo(f"Output directory: {voice_result['output_directory']}")
                    
                    click.echo("\nGenerated audio files:")
                    click.echo("-" * 40)
                    for i, audio_file in enumerate(voice_result['audio_files'], 1):
                        click.echo(f"{i}. {audio_file}")
                else:
                    click.echo(f"✗ Voice generation failed: {voice_result['error']}", err=True)
                    
            except Exception as e:
                click.echo(f"✗ Voice generation error: {str(e)}", err=True)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()