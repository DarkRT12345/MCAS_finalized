import sys
import os
import yt_dlp
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from language_tool_python import LanguageTool
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound
)
from faster_whisper import WhisperModel

DEBUG = False
# -------------------------
# INITIALIZE ONCE
# -------------------------
tool = LanguageTool('en-US')

MODEL_PATH = "C:/Users/User/Desktop/M_C_A_S/testcorrectmodel"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

summarizer = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer
)

# Whisper model loaded ONCE 
whisper_model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


# -------------------------
# AUDIO DOWNLOAD
# -------------------------
def download_audio(video_id, output_path="yt_audio"):
    import os
    import contextlib

    url = f"https://www.youtube.com/watch?v={video_id}"
    output_file = f"{output_path}.wav"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}.%(ext)s',  
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }

    # Silence stdout/stderr
    with open(os.devnull, 'w') as devnull, \
         contextlib.redirect_stdout(devnull), \
         contextlib.redirect_stderr(devnull):

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # Safety check
    if not os.path.exists(output_file):
        raise RuntimeError("Audio download failed (WAV file not created).")

    return output_file


# -------------------------
# WHISPER TRANSCRIPTION
# -------------------------
def transcribe_with_whisper(audio_path, language="en"):
    segments, _ = whisper_model.transcribe(audio_path, language=language)
    return " ".join(seg.text for seg in segments)


# -------------------------
# TRANSCRIPT FETCH
# -------------------------
def download_youtube_subtitle(video_id, language='en'):
    # FIRST TRY: YouTube captions
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript = transcripts.find_manually_created_transcript([language])
        except NoTranscriptFound:
            transcript = transcripts.find_generated_transcript([language])

        text = " ".join(entry['text'] for entry in transcript.fetch())
        if DEBUG:
            print("Transcript fetched from YouTube captions")
        return text

    except Exception as e:
        if DEBUG:
            print(f"YouTube captions failed: {e}")
            print("Falling back to Whisper...")

    # FALLBACK: Whisper
    try:
        audio_path = download_audio(video_id)
        text = transcribe_with_whisper(audio_path, language)
        os.remove(audio_path)  # cleanup ✅
        if DEBUG:
            print("Transcript generated using Whisper")
        return text

    except Exception as e:
        if DEBUG:
            print(f"Whisper transcription failed: {e}")

    return None


# -------------------------
# CHUNKING & SUMMARY
# -------------------------
def chunk_text(text, chunk_size=400):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


def summarize_text(text, max_length=150):
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=50,
        do_sample=False
    )
    return summary[0]['summary_text']


def post_process_summary(summary):
    return tool.correct(summary)


# -------------------------
# MAIN
# -------------------------
video_id = sys.argv[1]

transcript = download_youtube_subtitle(video_id)

if not transcript:
    if DEBUG:
        print("Failed to generate transcript.")
    sys.exit(1)

chunked_summary = []
for chunk in chunk_text(transcript):
    chunked_summary.append(summarize_text(chunk))

final_summary = " ".join(chunked_summary)
corrected_summary = post_process_summary(final_summary)

print(corrected_summary)

with open('summary.txt', 'w', encoding='utf-8') as f:
    f.write(corrected_summary)
