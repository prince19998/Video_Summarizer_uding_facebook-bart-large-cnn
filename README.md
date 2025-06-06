# Meeting Summarizer

A Flask-based web application that automatically transcribes and summarizes meeting recordings, extracting key points and action items.

## Features

- Upload and process audio/video meeting recordings
- Automatic transcription using OpenAI's Whisper
- Intelligent summarization using BART model
- Extraction of key points and action items
- Database storage for meeting records and summaries
- Simple and intuitive web interface

## Supported File Formats

- MP3
- MP4
- WAV
- M4A

## Prerequisites

- Python 3.7+
- Flask
- SQLite (or other SQL database)
- OpenAI Whisper
- Transformers (Hugging Face)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd meeting-summarizer
```

2. Create and activate a virtual environment:
```bash
python conda create -r deevenv python=3.11 -y
source conda activate deevenv/ # On Windows: activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.flaskenv` file with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
```

5. Initialize the database:
```bash
flask init-db
```

## Usage

1. Start the Flask application:
```bash
flask run
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a meeting recording file through the web interface

4. Wait for the processing to complete (transcription and summarization)

5. View the generated summary with key points and action items

## Project Structure

```
meeting-summarizer/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
├── uploads/           # Temporary file storage
└── instance/          # Instance-specific files
```

## Database Models

### Meeting
- `id`: Primary key
- `filename`: Name of the uploaded file
- `upload_time`: Timestamp of upload
- `status`: Processing status

### Summary
- `id`: Primary key
- `meeting_id`: Foreign key to Meeting
- `key_points`: Extracted key points
- `action_items`: Identified action items
- `generated_at`: Timestamp of summary generation

## Technologies Used

- Flask: Web framework
- SQLAlchemy: Database ORM
- OpenAI Whisper: Speech-to-text transcription
- Hugging Face Transformers: Text summarization
- SQLite: Database (default)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here] 