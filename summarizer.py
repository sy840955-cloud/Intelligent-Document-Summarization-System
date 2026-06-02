from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a smart document summarizer. Give concise bullet summary."},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
