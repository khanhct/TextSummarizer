"""
Example usage of PDF Text Summarizer
Demonstrates different ways to use the application programmatically.
"""

import os
import sys
from pathlib import Path
from main import PDFSummarizerApp
from utils import validate_pdf_file, format_duration, format_word_count
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """Example of basic PDF summarization."""
    print("=" * 60)
    print("EXAMPLE 1: Basic PDF Summarization")
    print("=" * 60)
    
    # Initialize the application
    app = PDFSummarizerApp()
    
    # Example PDF path (replace with your actual PDF)
    pdf_path = "sample_document.pdf"
    
    # Check if example PDF exists
    if not os.path.exists(pdf_path):
        print(f"Example PDF '{pdf_path}' not found.")
        print("Please place a PDF file named 'sample_document.pdf' in the current directory.")
        print("Or modify the pdf_path variable to point to your PDF file.")
        return
    
    try:
        # Process the PDF
        result = app.process_pdf(pdf_path, duration_minutes=15)
        
        # Display results
        print(f"✓ Successfully processed: {result['pdf_path']}")
        print(f"✓ Pages: {result['pdf_page_count']}")
        print(f"✓ Original words: {format_word_count(result['original_word_count'])}")
        print(f"✓ Summary words: {format_word_count(result['word_count'])}")
        print(f"✓ Estimated duration: {format_duration(result['estimated_duration_minutes'])}")
        
        print("\nSummary Preview:")
        print("-" * 40)
        preview = result['summary'][:300] + "..." if len(result['summary']) > 300 else result['summary']
        print(preview)
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def example_custom_duration():
    """Example of custom video duration."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Video Duration (10 minutes)")
    print("=" * 60)
    
    app = PDFSummarizerApp()
    pdf_path = "sample_document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Example PDF '{pdf_path}' not found.")
        return
    
    try:
        # Process for 10-minute video
        result = app.process_pdf(pdf_path, duration_minutes=10)
        
        print(f"✓ Target duration: {format_duration(10)}")
        print(f"✓ Actual duration: {format_duration(result['estimated_duration_minutes'])}")
        print(f"✓ Word count: {format_word_count(result['word_count'])}")
        
        print("\nKey Points:")
        print("-" * 40)
        for i, point in enumerate(result['key_points'], 1):
            print(f"{i}. {point}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def example_file_validation():
    """Example of file validation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: File Validation")
    print("=" * 60)
    
    # Test with different file types
    test_files = [
        "sample_document.pdf",
        "nonexistent.pdf",
        "README.md"  # Not a PDF
    ]
    
    for file_path in test_files:
        print(f"\nValidating: {file_path}")
        validation = validate_pdf_file(file_path)
        
        if validation['is_valid']:
            print("✓ File is valid")
            file_info = validation['file_info']
            print(f"  Size: {file_info['size_mb']} MB")
            print(f"  Name: {file_info['name']}")
        else:
            print("✗ File is invalid")
            for error in validation['errors']:
                print(f"  Error: {error}")
        
        if validation['warnings']:
            for warning in validation['warnings']:
                print(f"  Warning: {warning}")


def example_batch_processing():
    """Example of processing multiple PDFs."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Batch Processing")
    print("=" * 60)
    
    # Find all PDF files in current directory
    pdf_files = list(Path('.').glob('*.pdf'))
    
    if not pdf_files:
        print("No PDF files found in current directory.")
        print("Place some PDF files in the current directory to test batch processing.")
        return
    
    app = PDFSummarizerApp()
    
    for pdf_file in pdf_files[:3]:  # Process up to 3 files
        print(f"\nProcessing: {pdf_file.name}")
        try:
            result = app.process_pdf(str(pdf_file), duration_minutes=15)
            print(f"✓ Success: {format_word_count(result['word_count'])} words, "
                  f"{format_duration(result['estimated_duration_minutes'])}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")


def example_reading_metrics():
    """Example of reading metrics analysis."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Reading Metrics Analysis")
    print("=" * 60)
    
    app = PDFSummarizerApp()
    pdf_path = "sample_document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Example PDF '{pdf_path}' not found.")
        return
    
    try:
        result = app.process_pdf(pdf_path, duration_minutes=15)
        
        print("Reading Metrics:")
        print("-" * 40)
        
        metrics = result['reading_metrics']
        if metrics:
            print(f"Flesch Reading Ease: {metrics.get('flesch_reading_ease', 'N/A'):.2f}")
            print(f"Flesch-Kincaid Grade: {metrics.get('flesch_kincaid_grade', 'N/A'):.2f}")
            print(f"Automated Readability Index: {metrics.get('automated_readability_index', 'N/A'):.2f}")
            print(f"Coleman-Liau Index: {metrics.get('coleman_liau_index', 'N/A'):.2f}")
            
            # Interpret readability
            ease_score = metrics.get('flesch_reading_ease', 0)
            if ease_score >= 80:
                level = "Very Easy"
            elif ease_score >= 70:
                level = "Easy"
            elif ease_score >= 60:
                level = "Standard"
            elif ease_score >= 50:
                level = "Fairly Difficult"
            else:
                level = "Difficult"
            
            print(f"\nReadability Level: {level}")
        else:
            print("Reading metrics not available")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def main():
    """Run all examples."""
    print("PDF TEXT SUMMARIZER - EXAMPLE USAGE")
    print("=" * 60)
    print("This script demonstrates various ways to use the PDF Text Summarizer.")
    print("Make sure you have a PDF file named 'sample_document.pdf' in the current directory.")
    print("Or modify the examples to use your own PDF files.")
    
    # Run examples
    example_basic_usage()
    example_custom_duration()
    example_file_validation()
    example_batch_processing()
    example_reading_metrics()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETED")
    print("=" * 60)
    print("For more information, see README.md")
    print("For command-line usage: python main.py --help")


if __name__ == "__main__":
    main()
