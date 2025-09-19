# PDF Text Summarizer

A Python application that extracts text from PDF files and creates summaries optimized for 15-minute video content. Perfect for content creators, educators, and professionals who need to quickly understand and present PDF content.

## Features

- **PDF Text Extraction**: Robust text extraction using multiple methods (pdfplumber, PyPDF2)
- **OpenAI-Powered Summarization**: Uses GPT-3.5-turbo for high-quality, video-ready summaries
- **VBee Voice Generation**: Convert summaries to high-quality audio using VBee TTS API
- **Video-Optimized Output**: Summaries tailored for specific video durations (default: 15 minutes)
- **Key Points Extraction**: Automatically identifies important points for visual presentation
- **Reading Metrics**: Provides readability scores and estimated speaking time
- **CLI Interface**: Easy-to-use command-line interface with OpenAI and VBee API support
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Installation

### Option 1: Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone or download the project files**

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Activate the virtual environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

### Option 2: Using pip

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys (required):**
   
   **OpenAI API Key (for summarization):**
   ```bash
   # Windows
   set OPENAI_API_KEY=your_openai_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **VBee API Credentials (for voice generation):**
   ```bash
   # Windows
   set VBEE_TOKEN=your_vbee_token_here
   set VBEE_APP_ID=your_vbee_app_id_here
   
   # Linux/Mac
   export VBEE_TOKEN=your_vbee_token_here
   export VBEE_APP_ID=your_vbee_app_id_here
   ```
   
   **Option B: .env file**
   ```bash
   # Copy the template and add your API keys
   copy env_template.txt .env
   # Edit .env and add your actual API keys
   ```
   
   Get your API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - VBee: Contact VBee for TTS API access

4. **Download NLTK data (automatic on first run):**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('averaged_perceptron_tagger')
   ```

## Quick Start

### Basic Usage

**Using uv (Recommended):**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run the application
python main.py path/to/your/document.pdf

# Or run directly with uv
uv run python main.py path/to/your/document.pdf
```

**Using pip:**
```bash
python main.py path/to/your/document.pdf
```

### Advanced Usage

```bash
# Main application (PDF + Voice)
python main.py document.pdf --generate-voice --voice-output-dir ./audio

# Standalone summary tool
python summary_cli.py summarize-pdf document.pdf --output summary.txt --duration 10

# Standalone voice tool
python voice_cli.py generate-voice summary.txt --output-dir ./audio

# Use API keys from command line
python main.py document.pdf --api-key your_openai_key --vbee-token your_vbee_token --vbee-app-id your_app_id

# Custom voice settings
python main.py document.pdf --generate-voice --voice-code "female_voice" --speed-rate "1.2"

# Enable verbose logging
python main.py document.pdf --verbose
```

### Command Line Options

- `PDF_PATH`: Path to the PDF file to summarize (required)
- `--output, -o`: Output file path for the summary (optional)
- `--duration, -d`: Target video duration in minutes (default: 15)
- `--api-key`: OpenAI API key (optional, can use environment variable instead)
- `--generate-voice`: Generate voice audio from summary
- `--voice-output-dir`: Directory for voice audio files
- `--voice-code`: Voice code for TTS (optional)
- `--speed-rate`: Speech speed rate (default: 1.0)
- `--callback-url`: Callback URL for async voice processing (optional)
- `--vbee-token`: VBee API token (optional, can use environment variable instead)
- `--vbee-app-id`: VBee app ID (optional, can use environment variable instead)
- `--verbose, -v`: Enable verbose logging

## Example Output

The application generates a comprehensive summary file containing:

```
PDF TEXT SUMMARIZER - VIDEO READY SUMMARY
==================================================

Source PDF: document.pdf
Pages: 25
Original Word Count: 8,500
Summary Word Count: 2,325
Target Duration: 15.0 minutes
Processed: 2024-01-15T10:30:45

SUMMARY
--------------------
[Generated summary text optimized for 15-minute video presentation...]

KEY POINTS
--------------------
1. Main concept or finding
2. Important methodology
3. Key results or conclusions
4. Critical implications
5. Future directions

KEY TOPICS
--------------------
• research (mentioned 45 times)
• analysis (mentioned 32 times)
• methodology (mentioned 28 times)
• results (mentioned 25 times)
• conclusion (mentioned 18 times)

READING METRICS
--------------------
• Flesch Reading Ease: 65.50
• Flesch Kincaid Grade: 8.20
• Automated Readability Index: 7.80
• Coleman Liau Index: 9.10
```

## How It Works

### 1. PDF Text Extraction
- Uses `pdfplumber` for complex layouts and tables
- Falls back to `PyPDF2` for standard PDFs
- Handles multiple pages and various PDF formats

### 2. Text Preprocessing
- Removes PDF artifacts and formatting issues
- Normalizes whitespace and text structure
- Identifies sections and key topics

### 3. OpenAI-Powered Summarization
- **GPT-3.5-turbo**: Uses OpenAI's advanced language model for high-quality summaries
- **Video-Optimized Prompts**: Specifically designed for spoken presentation
- **Smart Chunking**: Handles large documents by splitting into manageable pieces
- **Length Optimization**: Automatically adjusts summary length for target video duration

### 4. Voice Generation (Optional)
- **VBee TTS Integration**: Converts summaries to high-quality audio
- **Smart Chunking**: Splits long summaries into manageable audio segments
- **Customizable Voice**: Supports different voice codes and speed rates
- **Batch Processing**: Generates multiple audio files for video production

### 5. Video Optimization
- Calculates target word count based on speaking rate (155 words/minute)
- Combines best summaries for optimal content
- Extracts key points for visual presentation

## Tool Architecture

The application is organized into modular tools for better maintainability:

### Summary Tool (`summary_tool.py`)
- **PDF Processing**: Extract text and create summaries
- **Text Summarization**: Direct text-to-summary conversion
- **File Management**: Save summaries with metadata
- **Statistics**: Provide summary analytics

### Voice Tool (`voice_tool.py`)
- **File-to-Voice**: Convert summary files to audio
- **Text-to-Voice**: Direct text-to-audio conversion
- **Voice Settings**: Customize voice parameters
- **Audio Management**: Organize and download audio files

### CLI Tools
- **`main.py`**: Complete workflow (PDF → Summary → Voice)
- **`summary_cli.py`**: Standalone summary operations
- **`voice_cli.py`**: Standalone voice generation

## Configuration

Edit `config.py` to customize:

- Default video duration
- Speaking rate (words per minute)
- Model parameters
- File size limits
- Output settings

## Requirements

- Python 3.8+
- PyPDF2 3.0.1
- pdfplumber 0.10.3
- openai 1.3.7
- nltk 3.8.1
- textstat 0.7.3
- click 8.1.7
- python-dotenv 1.0.0
- requests 2.31.0
- OpenAI API key (required)
- VBee API credentials (required for voice generation)

## File Structure

```
TextSummarizer/
├── main.py              # Main application entry point (PDF + Voice)
├── summary_tool.py      # Summary tool (PDF extraction + OpenAI summarization)
├── voice_tool.py        # Voice tool (VBee TTS integration)
├── summary_cli.py       # Standalone summary CLI
├── voice_cli.py         # Standalone voice generation CLI
├── pdf_extractor.py     # PDF text extraction module
├── text_summarizer.py   # OpenAI-powered text summarization
├── voice_generator.py  # VBee TTS voice generation
├── utils.py             # Utility functions
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── env_template.txt     # Environment variables template
├── demo.py              # Demo script with sample text
├── example_usage.py     # Usage examples
├── install.py           # Installation script
└── README.md           # This file
```

## Troubleshooting

### Common Issues

1. **"File not found" error**
   - Ensure the PDF file path is correct
   - Check file permissions

2. **"Insufficient text extracted" error**
   - PDF might be image-based (scanned document)
   - Try with a text-based PDF
   - Consider using OCR preprocessing

3. **Memory issues with large files**
   - Reduce file size or split into smaller sections
   - Increase system memory or use a more powerful machine

4. **OpenAI API issues**
   - Ensure you have a valid OpenAI API key
   - Check your OpenAI account billing and usage limits
   - Verify internet connection for API calls
   - Try running with `--verbose` for detailed error messages

### Performance Tips

- For large PDFs (>10MB), processing may take several minutes
- OpenAI API calls require internet connection
- Use SSD storage for better performance
- Close other applications to free up memory

## Use Cases

- **Educational Content**: Summarize research papers for lectures
- **Business Presentations**: Extract key points from reports
- **Content Creation**: Generate video scripts from documents
- **Research**: Quickly understand lengthy documents
- **Training Materials**: Create concise summaries for courses

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source and available under the MIT License.