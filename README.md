# MCAS - Multimedia Content Analyzing System

A comprehensive multimedia content analysis system that leverages advanced NLP models to summarize and analyze multimedia content with grammar correction and quality enhancement.

## Overview

MCAS is a Flask-based web application designed to analyze multimedia content through:
- **Text Summarization**: Intelligent summarization of long-form content using transformer-based models
- **Grammar Correction**: Automatic grammar and style correction using LanguageTool
- **Multi-chunk Processing**: Efficient processing of large texts through smart chunking

## Features

- 🔍 **Advanced Text Summarization**: Uses state-of-the-art seq2seq models for accurate content summarization
- ✏️ **Grammar & Style Correction**: Automatic detection and correction of grammatical errors
- 📦 **Chunked Processing**: Handles large documents by intelligently chunking text for optimal processing
- 🚀 **Web Interface**: User-friendly Flask web application
- 🔧 **Production Ready**: Includes Gunicorn for production deployment

## Tech Stack

- **Backend**: Flask 3.0.2, Gunicorn 21.2.0
- **NLP Models**: 
  - Transformers 4.39.3
  - PyTorch 2.5.1
  - SentencePiece 0.2.0
- **Text Processing**: Language Tool Python 2.7.1
- **Dependencies**: Protobuf 4.25.3, NumPy

## Project Structure

```
MCAS_finalized/
├── app.py                 # Main Flask application
├── testsummary.py         # Text summarization and grammar correction module
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates for web interface
├── static/                # Static assets (CSS, JavaScript, images)
└── README.md              # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DarkRT12345/MCAS_finalized.git
   cd MCAS_finalized
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download/Place the summarization model**
   - Ensure the summarization model is placed in `models/Summarizemodel/`
   - The model should be compatible with Hugging Face transformers

## Usage

### Running the Development Server

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Running with Gunicorn (Production)

```bash
gunicorn app:app
```

### Using the Summarization Module

```python
from testsummary import generate_summary

text = "Your long text here..."
summary = generate_summary(text)
print(summary)
```

## Key Components

### testsummary.py
This module handles:
- **Text Chunking**: Splits large texts into manageable chunks (default 500 words)
- **Summarization**: Generates concise summaries using transformer models
- **Post-processing**: Applies grammar correction to improve summary quality

**Main Functions:**
- `chunk_text(text, chunk_size=500)`: Splits text into chunks
- `summarize_text(text, max_length=150)`: Summarizes a text chunk
- `post_process_summary(summary)`: Applies grammar corrections
- `generate_summary(text)`: Full pipeline combining all steps

## Configuration

### Summarization Parameters
- **max_length**: Maximum length of generated summary (default: 150)
- **min_length**: Minimum length of generated summary (default: 50)
- **chunk_size**: Number of words per chunk (default: 500)

### Language Tool
- **Language**: English (US)
- **Server**: Remote API (https://api.languagetool.org/v2)

## Model Details

The system uses:
- **Seq2Seq Model**: Pre-trained transformer model for abstractive summarization
- **Tokenizer**: SentencePiece-based tokenizer for the summarization model
- **Grammar Checker**: Language Tool with English US locale

## Performance Considerations

- Large documents are automatically chunked to prevent memory issues
- Each chunk is summarized independently, then concatenated
- Grammar correction is applied to the final summary
- Consider the GPU availability for faster inference with PyTorch

## Future Enhancements

- Multi-language support
- Custom model training capabilities
- API endpoint documentation
- Batch processing support
- Result caching mechanism
- Web UI improvements with progress tracking

## License

This project is available on GitHub at [DarkRT12345/MCAS_finalized](https://github.com/DarkRT12345/MCAS_finalized)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Note**: Ensure you have appropriate GPU resources for optimal performance with the transformer models. CPU inference is supported but will be slower.