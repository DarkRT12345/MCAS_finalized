from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from language_tool_python import LanguageTool

# Load once when imported
model_path = "models/Summarizemodel"
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

tool = LanguageTool('en-US', remote_server='https://api.languagetool.org/v2')

def chunk_text(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def summarize_text(text, max_length=150):
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def post_process_summary(summary):
    return tool.correct(summary)

def generate_summary(text):
    chunked_summary = [summarize_text(chunk) for chunk in chunk_text(text, chunk_size=500)]
    final_summary = " ".join(chunked_summary)
    corrected_summary = post_process_summary(final_summary)
    return corrected_summary
