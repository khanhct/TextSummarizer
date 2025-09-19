# Quick Setup Guide - PDF Text Summarizer with OpenAI

## 🚀 Quick Start (5 minutes)

**Note**: This application requires an OpenAI API key to function.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in to your OpenAI account
3. Create a new API key
4. Copy the key (it starts with `sk-`)

### 3. Set Up API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows
set OPENAI_API_KEY=sk-your-actual-api-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Option B: .env File**
```bash
# Copy template
copy env_template.txt .env

# Edit .env file and add your API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Option C: Command Line (Less Secure)**
```bash
python main.py document.pdf --api-key sk-your-actual-api-key-here
```

### 4. Test the Application
```bash
# Run demo with sample text
python demo.py

# Process a PDF file
python main.py your_document.pdf
```

## 💡 Usage Examples

### Basic Usage
```bash
python main.py document.pdf
```

### Advanced Usage
```bash
# Custom duration and output file
python main.py document.pdf --duration 10 --output my_summary.txt

# With verbose logging
python main.py document.pdf --verbose
```

### Batch Processing
```bash
# Process multiple PDFs
python example_usage.py
```

## 🔧 Troubleshooting

### "OpenAI API key not found"
- Make sure you've set the OPENAI_API_KEY environment variable
- Or use the --api-key option
- Check that your API key is valid and has credits

### "Rate limit exceeded"
- You've hit OpenAI's rate limits
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

### "Quota exceeded"
- Your OpenAI account has run out of credits
- Add credits to your OpenAI account
- Check your usage at https://platform.openai.com/usage

### Application fails without OpenAI API key
- OpenAI API key is required for the application to work
- No fallback methods are available
- Ensure your API key is valid and has credits

## 📊 Cost Estimation

OpenAI GPT-3.5-turbo pricing (as of 2024):
- Input: ~$0.0015 per 1K tokens
- Output: ~$0.002 per 1K tokens

For a typical PDF:
- 10-page document ≈ $0.01-0.05
- 50-page document ≈ $0.05-0.25

## 🎯 Tips for Best Results

1. **Ensure OpenAI API key is set** - required for the application to work
2. **Clean PDFs work best** (avoid scanned documents)
3. **Text-based PDFs** are preferred over image-based
4. **Adjust duration** based on your video needs
5. **Monitor API usage** to avoid exceeding quotas

## 📞 Support

- Check the main README.md for detailed documentation
- Run `python main.py --help` for command options
- Use `--verbose` flag for detailed error messages
