import os
from flask import Flask, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
import json
import requests

app = Flask(__name__)
CORS(app)
PORT = os.getenv('PORT',8000)
NLP = spacy.load("en_core_web_sm")
API_KEY = json.load(open("config.json"))


def get_transcript(video_id, percent):
    transcript = None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except:
        return {"error": "No Trasncript found"}
    transcript_string = ""
    for line in transcript:
        transcript_string += line["text"] + " "
    
    return get_summary(transcript_string, percent)

def get_summary(transcript, percent):
    document = NLP(transcript)
    article = ""
    num_sentences = 0
    for sentence in document.sents:
        article += sentence.text+".\n "
        num_sentences += 1
    summary_length= round(float(percent)*num_sentences)
    
    api_url= ("http://api.smmry.com/&SM_API_KEY=%s&SM_LENGTH=%s" 
			% (API_KEY,summary_length))
    r = requests.post(api_url, data={"sm_api.input":article})

    if "sm_api_content" not in r.json():
        return {"error":"No transcript found, or transcript too short!"}
    return {"result":r.json()["sm_api_content"]}

@app.route("/")
def endpoint():
    return "Welcome to tldw"

@app.route("/summarize")
def summarize():
    video_id = request.args.get("video_id")
    percentage = request.args.get("percentage")
    response = get_transcript(video_id, percentage)
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)