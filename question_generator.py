import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_questions(resume_text):

    prompt = f"""
    Based on the following resume:

    {resume_text}

    Generate:

    - 5 HR questions
    - 5 Technical questions
    - 3 Project questions

    Return ONLY valid JSON in this format:

    {{
      "hr": [
        "question1",
        "question2"
      ],
      "technical": [
        "question1",
        "question2"
      ],
      "projects": [
        "question1",
        "question2"
      ]
    }}

    Do not include markdown.
    Do not include ```json.
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove accidental markdown
    text = text.replace("```json", "")
    text = text.replace("```", "")

    questions = json.loads(text)

    return questions