"""
Voice Generation CLI Tool
Command-line interface for generating voice from summary files using VBee TTS API.
"""

import click
import os
import sys
import logging
from pathlib import Path
from voice_tool import VoiceTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument('summary_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for audio files')
@click.option('--voice-code', '-v', default='', help='Voice code for TTS (optional)')
@click.option('--speed-rate', '-s', default='1.0', help='Speech speed rate (default: 1.0)')
@click.option('--callback-url', '-c', default='', help='Callback URL for async processing (optional)')
@click.option('--token', help='VBee API token (or set VBEE_TOKEN environment variable)')
@click.option('--app-id', help='VBee app ID (or set VBEE_APP_ID environment variable)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def generate_voice(summary_file, output_dir, voice_code, speed_rate, callback_url, token, app_id, verbose):
    """
    Generate voice audio from summary file using VBee TTS API.
    
    SUMMARY_FILE: Path to the summary text file to convert to speech
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize voice tool
        click.echo("Initializing VBee TTS client...")
        voice_tool = VoiceTool(vbee_token=token, vbee_app_id=app_id)
        click.echo("✓ VBee TTS client initialized successfully")
        
        # Generate voice
        click.echo(f"Processing summary file: {summary_file}")
        click.echo(f"Voice code: {voice_code or 'default'}")
        click.echo(f"Speed rate: {speed_rate}")
        
        result = voice_tool.generate_voice_from_file(
            summary_file_path=summary_file,
            output_dir=output_dir,
            voice_code=voice_code,
            speed_rate=speed_rate,
            callback_url=callback_url
        )
        
        if result['success']:
            click.echo("\n" + "="*60)
            click.echo("VOICE GENERATION COMPLETED SUCCESSFULLY!")
            click.echo("="*60)
            click.echo(f"Summary file: {result['summary_file']}")
            click.echo(f"Total sections: {result['total_sections']}")
            click.echo(f"Audio files generated: {len(result['audio_files'])}")
            click.echo(f"Output directory: {result['output_directory']}")
            
            click.echo("\nGenerated audio files:")
            click.echo("-" * 40)
            for i, audio_file in enumerate(result['audio_files'], 1):
                click.echo(f"{i}. {audio_file}")
            
            click.echo(f"\nTotal audio files: {len(result['audio_files'])}")
            
        else:
            click.echo(f"✗ Voice generation failed: {result['error']}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@click.command()
@click.argument('text', type=str)
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for audio files')
@click.option('--voice-code', '-v', default='', help='Voice code for TTS (optional)')
@click.option('--speed-rate', '-s', default='1.0', help='Speech speed rate (default: 1.0)')
@click.option('--callback-url', '-c', default='', help='Callback URL for async processing (optional)')
@click.option('--token', help='VBee API token (or set VBEE_TOKEN environment variable)')
@click.option('--app-id', help='VBee app ID (or set VBEE_APP_ID environment variable)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def generate_voice_from_text(text, output_dir, voice_code, speed_rate, callback_url, token, app_id, verbose):
    """
    Generate voice audio directly from text using VBee TTS API.
    
    TEXT: Text to convert to speech
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize voice tool
        click.echo("Initializing VBee TTS client...")
        voice_tool = VoiceTool(vbee_token=token, vbee_app_id=app_id)
        click.echo("✓ VBee TTS client initialized successfully")
        
        # Generate voice
        click.echo(f"Processing text ({len(text)} characters)")
        click.echo(f"Voice code: {voice_code or 'default'}")
        click.echo(f"Speed rate: {speed_rate}")
        
        result = voice_tool.generate_voice_from_text(
            text=text,
            output_dir=output_dir,
            voice_code=voice_code,
            speed_rate=speed_rate,
            callback_url=callback_url
        )
        
        if result['success']:
            click.echo("\n" + "="*60)
            click.echo("VOICE GENERATION COMPLETED SUCCESSFULLY!")
            click.echo("="*60)
            click.echo(f"Text length: {len(text)} characters")
            click.echo(f"Total chunks: {result['total_chunks']}")
            click.echo(f"Audio files generated: {len(result['audio_files'])}")
            click.echo(f"Output directory: {result['output_directory']}")
            
            click.echo("\nGenerated audio files:")
            click.echo("-" * 40)
            for i, audio_file in enumerate(result['audio_files'], 1):
                click.echo(f"{i}. {audio_file}")
            
            click.echo(f"\nTotal audio files: {len(result['audio_files'])}")
            
        else:
            click.echo(f"✗ Voice generation failed: {result['error']}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@click.group()
def voice():
    """Voice Generation CLI - Convert text to speech using VBee TTS API."""
    pass


voice.add_command(generate_voice)
voice.add_command(generate_voice_from_text)


if __name__ == '__main__':
    voice()
