"""
Summary CLI Tool
Command-line interface for PDF text summarization using OpenAI.
"""

import click
import os
import sys
import logging
from pathlib import Path
from summary_tool import SummaryTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('summary_tool.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path for the summary')
@click.option('--duration', '-d', default=15, help='Target video duration in minutes (default: 15)')
@click.option('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def summarize_pdf(pdf_path, output, duration, api_key, verbose):
    """
    Summarize PDF file using OpenAI.
    
    PDF_PATH: Path to the PDF file to summarize
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize summary tool
        click.echo("Initializing OpenAI client...")
        summary_tool = SummaryTool(openai_api_key=api_key)
        
        if not summary_tool.is_openai_available():
            click.echo("Error: OpenAI API key is required.")
            click.echo("Please set OPENAI_API_KEY environment variable or use --api-key option")
            click.echo("Get your API key from: https://platform.openai.com/api-keys")
            sys.exit(1)
        
        click.echo("✓ OpenAI client initialized successfully")
        
        # Generate output path if not provided
        if not output:
            pdf_name = Path(pdf_path).stem
            output = f"{pdf_name}_summary_{duration}min.txt"
        
        # Process PDF
        click.echo(f"Processing PDF: {pdf_path}")
        click.echo(f"Target duration: {duration} minutes")
        click.echo("Extracting text and creating summary...")
        
        result = summary_tool.process_pdf(pdf_path, output, duration)
        
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
        
        # Display summary stats
        stats = summary_tool.get_summary_stats(result)
        click.echo(f"\nCompression ratio: {stats['compression_ratio']}:1")
        click.echo(f"Key points: {stats['key_points_count']}")
        click.echo(f"Key topics: {stats['key_topics_count']}")
        
        click.echo("\nSUMMARY PREVIEW:")
        click.echo("-" * 40)
        preview = result['summary'][:500] + "..." if len(result['summary']) > 500 else result['summary']
        click.echo(preview)
        
        click.echo("\nKEY POINTS:")
        click.echo("-" * 40)
        for i, point in enumerate(result['key_points'], 1):
            click.echo(f"{i}. {point}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@click.command()
@click.argument('text', type=str)
@click.option('--output', '-o', type=click.Path(), help='Output file path for the summary')
@click.option('--duration', '-d', default=15, help='Target video duration in minutes (default: 15)')
@click.option('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def summarize_text(text, output, duration, api_key, verbose):
    """
    Summarize text directly using OpenAI.
    
    TEXT: Text content to summarize
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize summary tool
        click.echo("Initializing OpenAI client...")
        summary_tool = SummaryTool(openai_api_key=api_key)
        
        if not summary_tool.is_openai_available():
            click.echo("Error: OpenAI API key is required.")
            click.echo("Please set OPENAI_API_KEY environment variable or use --api-key option")
            click.echo("Get your API key from: https://platform.openai.com/api-keys")
            sys.exit(1)
        
        click.echo("✓ OpenAI client initialized successfully")
        
        # Generate output path if not provided
        if not output:
            output = f"text_summary_{duration}min.txt"
        
        # Process text
        click.echo(f"Processing text ({len(text.split())} words)")
        click.echo(f"Target duration: {duration} minutes")
        click.echo("Creating summary...")
        
        result = summary_tool.summarize_text(text, duration, output)
        
        # Display results
        click.echo("\n" + "="*60)
        click.echo("SUMMARY COMPLETED SUCCESSFULLY!")
        click.echo("="*60)
        click.echo(f"Original words: {result['original_word_count']}")
        click.echo(f"Summary words: {result['word_count']}")
        click.echo(f"Estimated duration: {result['estimated_duration_minutes']} minutes")
        click.echo(f"Summarization method: {result.get('summarization_method', 'openai').upper()}")
        click.echo(f"Summary saved to: {output}")
        
        # Display summary stats
        stats = summary_tool.get_summary_stats(result)
        click.echo(f"\nCompression ratio: {stats['compression_ratio']}:1")
        click.echo(f"Key points: {stats['key_points_count']}")
        click.echo(f"Key topics: {stats['key_topics_count']}")
        
        click.echo("\nSUMMARY PREVIEW:")
        click.echo("-" * 40)
        preview = result['summary'][:500] + "..." if len(result['summary']) > 500 else result['summary']
        click.echo(preview)
        
        click.echo("\nKEY POINTS:")
        click.echo("-" * 40)
        for i, point in enumerate(result['key_points'], 1):
            click.echo(f"{i}. {point}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@click.group()
def summary():
    """Summary CLI - PDF and text summarization using OpenAI."""
    pass


summary.add_command(summarize_pdf)
summary.add_command(summarize_text)


if __name__ == '__main__':
    summary()
