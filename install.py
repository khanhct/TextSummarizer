"""
Installation script for PDF Text Summarizer
Handles dependency installation and setup.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required")
        print(f"  Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required Python packages."""
    print("\nInstalling dependencies...")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("✗ requirements.txt not found")
        return False
    
    # Install packages
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )
    
    return success


def download_nltk_data():
    """Download required NLTK data."""
    print("\nDownloading NLTK data...")
    
    nltk_script = """
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    print("NLTK data downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")
    exit(1)
"""
    
    success = run_command(
        f"{sys.executable} -c \"{nltk_script}\"",
        "Downloading NLTK data"
    )
    
    return success


def test_installation():
    """Test if the installation works."""
    print("\nTesting installation...")
    
    test_script = """
try:
    from pdf_extractor import PDFExtractor
    from text_summarizer import TextSummarizer
    from main import PDFSummarizerApp
    print("✓ All modules imported successfully")
    
    # Test OpenAI integration
    try:
        summarizer = TextSummarizer()
        print("✓ OpenAI integration ready")
    except Exception as e:
        print("⚠ OpenAI API key not found")
        print("  Set OPENAI_API_KEY environment variable - this is required for the application to work")
        print(f"  Error: {str(e)}")
        
except ImportError as e:
    print(f"✗ Import error: {e}")
    exit(1)
"""
    
    success = run_command(
        f"{sys.executable} -c \"{test_script}\"",
        "Testing module imports"
    )
    
    return success


def create_sample_files():
    """Create sample files for testing."""
    print("\nCreating sample files...")
    
    # Create a sample PDF (text file for demonstration)
    sample_content = """
This is a sample document for testing the PDF Text Summarizer.

Introduction:
This document demonstrates the capabilities of the PDF Text Summarizer application.
It shows how the system can extract text from PDF files and create summaries
optimized for video content.

Main Points:
1. The application uses multiple extraction methods for robust text processing
2. AI-powered summarization creates high-quality content summaries
3. Video optimization ensures appropriate length for target duration
4. Key points extraction helps with visual presentation

Methodology:
The summarization process involves several steps:
- Text extraction from PDF files
- Preprocessing and cleaning
- Multi-method summarization
- Video optimization
- Key points extraction

Results:
The system successfully processes PDF documents and creates summaries
suitable for video presentations. The output includes reading metrics,
key topics, and estimated speaking time.

Conclusion:
The PDF Text Summarizer is a powerful tool for content creators,
educators, and professionals who need to quickly understand and
present PDF content in video format.
"""
    
    try:
        with open("sample_document.txt", "w", encoding="utf-8") as f:
            f.write(sample_content)
        print("✓ Created sample_document.txt")
        print("  Note: This is a text file for demonstration. Replace with actual PDF for testing.")
    except Exception as e:
        print(f"✗ Error creating sample file: {e}")


def main():
    """Main installation process."""
    print("PDF TEXT SUMMARIZER - INSTALLATION")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Installation failed at dependency installation step")
        sys.exit(1)
    
    # Download NLTK data
    if not download_nltk_data():
        print("\n✗ Installation failed at NLTK data download step")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n✗ Installation failed at testing step")
        sys.exit(1)
    
    # Create sample files
    create_sample_files()
    
    print("\n" + "=" * 50)
    print("INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Set up OpenAI API key (REQUIRED):")
    print("   - Get API key from: https://platform.openai.com/api-keys")
    print("   - Set environment variable: OPENAI_API_KEY=your_key_here")
    print("   - Or copy env_template.txt to .env and add your key")
    print("   - The application will not work without this API key")
    print("2. Place a PDF file in the current directory")
    print("3. Run: python main.py your_document.pdf")
    print("4. Or run: python demo.py for a quick test")
    print("\nFor help: python main.py --help")
    print("For setup guide: see SETUP_GUIDE.md")


if __name__ == "__main__":
    main()
