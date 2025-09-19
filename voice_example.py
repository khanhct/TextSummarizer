"""
Voice Generation Example
Demonstrates how to use the voice generation functionality.
"""

import os
import sys
from voice_tool import VoiceTool
from summary_tool import SummaryTool


def example_voice_from_file():
    """Example of generating voice from a summary file."""
    print("=" * 60)
    print("EXAMPLE 1: Generate Voice from Summary File")
    print("=" * 60)
    
    # Check if we have VBee credentials
    if not os.getenv('VBEE_TOKEN') or not os.getenv('VBEE_APP_ID'):
        print("VBee credentials not found!")
        print("Please set VBEE_TOKEN and VBEE_APP_ID environment variables")
        print("Example:")
        print("  set VBEE_TOKEN=your_token_here")
        print("  set VBEE_APP_ID=your_app_id_here")
        return
    
    # Example summary file (create one if it doesn't exist)
    summary_file = "example_summary.txt"
    if not os.path.exists(summary_file):
        print(f"Creating example summary file: {summary_file}")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("""SUMMARY
--------------------
This is an example summary for voice generation testing. The PDF Text Summarizer 
has successfully extracted and summarized content from a document. The summary 
includes key points, main concepts, and important findings. This text will be 
converted to speech using the VBee TTS API for video production purposes.

The application supports multiple voice options, speed adjustments, and can 
generate audio files in different formats. Users can customize the voice 
generation process according to their specific requirements.

KEY POINTS
--------------------
1. PDF text extraction and summarization
2. OpenAI-powered content analysis
3. VBee TTS voice generation
4. Video-ready audio output
5. Customizable voice settings
""")
    
    try:
        # Initialize voice tool
        print("Initializing VBee TTS client...")
        voice_tool = VoiceTool()
        print("✓ VBee TTS client initialized successfully")
        
        # Generate voice
        print(f"Generating voice from: {summary_file}")
        result = voice_tool.generate_voice_from_file(
            summary_file_path=summary_file,
            output_dir="./voice_output",
            voice_code="",  # Use default voice
            speed_rate="1.0"
        )
        
        if result['success']:
            print("✓ Voice generation completed successfully!")
            print(f"Audio files generated: {len(result['audio_files'])}")
            print(f"Output directory: {result['output_directory']}")
            
            print("\nGenerated audio files:")
            print("-" * 40)
            for i, audio_file in enumerate(result['audio_files'], 1):
                print(f"{i}. {audio_file}")
        else:
            print(f"✗ Voice generation failed: {result['error']}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def example_voice_from_text():
    """Example of generating voice directly from text."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Generate Voice from Text")
    print("=" * 60)
    
    # Check if we have VBee credentials
    if not os.getenv('VBEE_TOKEN') or not os.getenv('VBEE_APP_ID'):
        print("VBee credentials not found!")
        print("Please set VBEE_TOKEN and VBEE_APP_ID environment variables")
        return
    
    # Sample text
    sample_text = """
    Welcome to the PDF Text Summarizer with Voice Generation. This application 
    combines the power of OpenAI's GPT-3.5-turbo for text summarization with 
    VBee's high-quality text-to-speech technology. You can now convert your PDF 
    documents into both written summaries and audio files, making it perfect for 
    creating video content, podcasts, or educational materials.
    
    The voice generation feature supports multiple voice options, adjustable 
    speech rates, and can handle long documents by automatically splitting them 
    into manageable audio segments. This makes it ideal for content creators 
    who need professional-quality audio for their projects.
    """
    
    try:
        # Initialize voice tool
        print("Initializing VBee TTS client...")
        voice_tool = VoiceTool()
        print("✓ VBee TTS client initialized successfully")
        
        # Generate voice
        print(f"Generating voice from text ({len(sample_text)} characters)")
        result = voice_tool.generate_voice_from_text(
            text=sample_text,
            output_dir="./voice_output",
            voice_code="",  # Use default voice
            speed_rate="1.0"
        )
        
        if result['success']:
            print("✓ Voice generation completed successfully!")
            print(f"Audio files generated: {len(result['audio_files'])}")
            print(f"Output directory: {result['output_directory']}")
            
            print("\nGenerated audio files:")
            print("-" * 40)
            for i, audio_file in enumerate(result['audio_files'], 1):
                print(f"{i}. {audio_file}")
        else:
            print(f"✗ Voice generation failed: {result['error']}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def example_cli_usage():
    """Example of using the CLI commands."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: CLI Usage Examples")
    print("=" * 60)
    
    print("Command line examples:")
    print("-" * 40)
    
    print("1. Generate voice from summary file:")
    print("   python voice_cli.py generate-voice example_summary.txt --output-dir ./audio")
    
    print("\n2. Generate voice from text:")
    print("   python voice_cli.py generate-voice-from-text \"Hello world\" --output-dir ./audio")
    
    print("\n3. Custom voice settings:")
    print("   python voice_cli.py generate-voice example_summary.txt --voice-code female --speed-rate 1.2")
    
    print("\n4. Using API keys from command line:")
    print("   python voice_cli.py generate-voice example_summary.txt --token your_token --app-id your_app_id")
    
    print("\n5. Main application with voice generation:")
    print("   python main.py document.pdf --generate-voice --voice-output-dir ./audio")
    
    print("\n6. Standalone summary tool:")
    print("   python summary_cli.py summarize-pdf document.pdf --output summary.txt")


def main():
    """Run all voice generation examples."""
    print("VOICE GENERATION EXAMPLES")
    print("=" * 60)
    print("This script demonstrates voice generation functionality.")
    print("Make sure you have VBee API credentials set up.")
    
    # Run examples
    example_voice_from_file()
    example_voice_from_text()
    example_cli_usage()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETED")
    print("=" * 60)
    print("For more information, see README.md")
    print("For CLI usage: python voice_cli.py --help")


if __name__ == "__main__":
    main()
