import PyPDF2
import google.generativeai as genai
import json
import os

def extract_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_quiz(pdf_text, subject_name):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Based on this {subject_name} study material:
    {pdf_text[:3000]}

    Generate 10 multiple choice questions.
    Return ONLY a JSON array, no extra text, no markdown:
    [
        {{
            "question": "...",
            "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
            "correct": "A",
            "topic": "..."
        }}
    ]
    """

    response = model.generate_content(prompt)
    text = response.text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text)

def get_weak_topics(quiz_results):
    weak = {}
    for result in quiz_results:
        for topic in result.weak_topics:
            weak[topic] = weak.get(topic, 0) + 1

    sorted_weak = sorted(weak.items(), key=lambda x: x[1], reverse=True)
    return [topic for topic, count in sorted_weak]