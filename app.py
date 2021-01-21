import os
from flask import Flask, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from summarizer import Summarizer

app = Flask(__name__)
CORS(app)
PORT = os.getenv('PORT',8000)
NLP = spacy.load("en_core_web_sm")

def get_transcript(video_id):
    transcript = None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except:
        return {"error": "No Trasncript found"}
    transcript_string = ""
    for line in transcript:
        transcript_string += line["text"] + " "
    
    return get_summary(transcript_string)

def get_summary(transcript):
    document = NLP(transcript)
    article = ""
    for sentence in document.sents:
        article += sentence.text+".\n "
    model = Summarizer()
    summary = model(article, min_length=20)
    result = "".join(summary)
    return {"result" : result}

@app.route("/")
def endpoint():
    return "Welcome to tldw"

@app.route("/summarize")
def summarize():
    video_id = request.args.get("video_id")
    response = get_transcript("nl7kDPYD20A")
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)