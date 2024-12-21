# MyPodify

MyPodify is an open-source local solution for automatically generating podcasts from documents. Think of it as a self-hosted alternative to Google's NotebookLM, focused on podcast creation. The tool processes documents from a specified folder and transforms them into engaging podcast content complete with outlines, scripts, and audio.

## Features

- **Document Processing**: Supports multiple file formats including PDF (via Azure Document Intelligence), DOCX, and TXT files
- **Automated Content Generation**: Creates podcast outlines and scripts using Ollama AI
- **Text-to-Speech**: Converts scripts into audio using Azure's Speech Service
- **Multiple Host Support**: Generate content for 1-3 hosts (default: 2 hosts - Alex and Jane)
- **Project Organization**: Automatically creates organized directory structure for outputs
- **Detailed Logging**: Comprehensive logging system for troubleshooting

## Prerequisites

- Python 3.7+
- Azure Account (for PDF processing and Speech Services)
- Ollama. Download Ollama [here](http://ollama.com)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mypodify.git
cd mypodify
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following:
```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key

AZURE_TTS_ENDPOINT=your_endpoint
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=your_region
```

## Usage

1. Place your source documents in the `my_docs` directory

2. Run the podcast generator:
```bash
python main.py
```

3. Follow the prompts to:
   - Specify output directory (default: 'output')
   - Enter project name
   - Set number of hosts (default: 2)
   - Provide project description (optional)

## Project Structure

```
mypodify/
├── __pycache__/            # Python cache files
├── ai_helper/              # AI content generation modules
│   ├── __pycache__/
│   ├── ai_helper.py        # Core AI helper functions
│   ├── generate_outline.py # Podcast outline generation
│   ├── generate_speech.py  # Speech synthesis module
│   └── script_generator.py # Podcast script generation
├── logs/                   # Log files directory
├── my_docs/                # Input documents directory
├── output/                 # Generated content directory
├── utils/                  # Utility functions
│   ├── __pycache__/
│   └── combine_audio.py    # Audio processing utilities
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── document_processor.py   # Document processing module
├── helpers.py             # Helper utilities
├── logger.py              # Logging configuration
├── main.py                # Main application entry
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
```

## Output Structure

Each project generates:
- Processed document text files
- Markdown outline files
- Podcast scripts in Markdown format
- Individual audio segments
- Combined final podcast audio file
- Project metadata JSON

## Supported File Types

- PDF (requires Azure Document Intelligence)
- DOCX
- TXT
- DOC (currently unsupported, must be converted to DOCX)

## Configuration

The system can be configured through various parameters:

- **Host Count**: 1-3 hosts (affects conversation style and dynamics)
- **Output Directory**: Customizable output location
- **Project Name**: Used for organizing outputs
- **Description**: Optional context for content generation

## Logging

The system includes comprehensive logging:
- General logs: `podcast_generator.log`
- Document processing logs: `document_processor.log`
- Speech generation logs: `speech_generator.log`
- Outline generation logs: `podcast_outline.log`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Azure Document Intelligence for PDF processing
- Azure Speech Services for text-to-speech
- Ollama for AI content generation

## Note

This is an early version of the project and is under active development. Features and functionality may change in future releases.

## Contact

For questions or feedback or issues, please create an issue.
