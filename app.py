from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import whisper
from transformers import pipeline
from models import db, Meeting, Summary
from config import Config
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file uploaded")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected")
        
        if not allowed_file(file.filename):
            return render_template('index.html', error="File type not supported")
        
        try:
            # Save file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Create meeting record
            meeting = Meeting(
                filename=filename,
                upload_time=datetime.utcnow(),
                status="processing"
            )
            db.session.add(meeting)
            db.session.commit()
            
            # Transcribe audio
            model = whisper.load_model("base")
            result = model.transcribe(filepath)
            transcript = result["text"]
            
            # Generate summary
            summary = generate_summary(transcript)
            
            # Save summary
            summary_record = Summary(
                meeting_id=meeting.id,
                key_points=summary["key_points"],
                action_items=summary["action_items"],
                generated_at=datetime.utcnow()
            )
            db.session.add(summary_record)
            meeting.status = "completed"
            db.session.commit()
            
            # Clean up
            os.remove(filepath)
            
            return render_template('index.html', summary=summary)
            
        except Exception as e:
            if 'meeting' in locals():
                meeting.status = "failed"
                db.session.commit()
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'mp3', 'mp4', 'wav', 'm4a'}

def generate_summary(text):
    # First summarize the content
    summary_result = summarizer(text, max_length=150, min_length=30, do_sample=False)
    summarized_text = summary_result[0]['summary_text']
    
    # Then extract action items
    prompt = f"""
    Extract action items from this meeting summary. Format as a JSON list under "action_items":
    {summarized_text}
    """
    
    action_items_result = summarizer(prompt, max_length=150, min_length=30, do_sample=False)
    action_items_text = action_items_result[0]['summary_text']
    
    try:
        action_items = json.loads(action_items_text)
    except json.JSONDecodeError:
        action_items = {"action_items": [action_items_text]}
    
    return {
        "key_points": [summarized_text],
        "action_items": action_items.get("action_items", [])
    }

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
    print("Database initialized.")

if __name__ == '__main__':
    app.run()