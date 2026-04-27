import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(review: str) -> str:
    return f"""You are a product review analysis engine.

Analyze the customer review below and return a JSON object with EXACTLY these 4 fields:

1. "sentiment"       → One word only: Positive, Negative, Mixed, or Neutral
2. "sentiment_score" → A float between 0.0 (most negative) and 1.0 (most positive)
3. "key_points"      → A list of 2-5 short phrases extracted strictly from the review
4. "summary"         → One professional sentence summarizing the key opinion in neutral, specific language. Must mention the product and main reason for sentiment.

STRICT RULES:
- Return ONLY the raw JSON object. No markdown, no code blocks, no explanation.
- Do not add any information not present in the review.
- key_points must be extracted from the review, not invented.
- summary must be one sentence, maximum 30 words.

Customer Review:
\"\"\"{review}\"\"\"

JSON Response:"""


def analyze_review(review: str) -> dict:
    review = review.strip()

    if not review:
        raise ValueError("Review text cannot be empty.")

    if len(review) < 10:
        raise ValueError("Review is too short to analyze.")

    prompt = build_prompt(review)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a product review analysis engine. Always respond with raw JSON only. No markdown, no explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=500
    )

    raw_text = response.choices[0].message.content.strip()

    # Defensive cleaning
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    result = json.loads(raw_text)

    required_fields = ["sentiment", "sentiment_score", "key_points", "summary"]
    for field in required_fields:
        if field not in result:
            raise KeyError(f"Missing field in response: {field}")

    return result