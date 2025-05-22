# Slide Search App

A powerful application for searching and analyzing presentation slides using AI-powered embeddings and hybrid search capabilities.

## Features

- Upload and process PowerPoint (PPTX) and PDF presentations
- Extract text and images from slides
- Generate embeddings for both text and images
- OCR support for image-only slides
- Hybrid search combining vector and keyword search
- Modern web interface for searching and viewing slides
- Docker support for easy deployment

## Project Structure

```
slide-search-app/
├── README.md
├── requirements.txt
├── config/                 # Configuration files
├── data/                  # Data storage
├── src/                   # Source code
├── web-ui/               # Frontend application
└── docker/               # Docker configuration
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```
1.b. # Install LibreOffice (macOS via Homebrew)
brew install --cask libreoffice

2. Configure environment variables:
- Create a `.env` file based on `.env.example`
- Set up Weaviate connection details
- Configure storage settings

3. Run the application:
```bash
# Start the backend
python src/api/main.py

# Start the frontend (in web-ui directory)
npm install
npm run dev
```

## Docker Deployment

```bash
docker-compose up --build
```

## License

MIT 