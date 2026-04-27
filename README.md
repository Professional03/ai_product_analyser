# Product Review Sentiment Analyzer

An AI-powered system that analyzes customer reviews and returns 
structured sentiment analysis using LLM prompt engineering.

## Features
- Sentiment classification (Positive / Negative / Mixed / Neutral)
- Sentiment score (0.0 - 1.0)
- Key point extraction strictly from review content
- Professional one-sentence summary

## Tech Stack
- Python, Streamlit
- Groq API (LLaMA 3.3 70B)
- Prompt Engineering for structured JSON output

## Run Locally
pip install -r requirements.txt
streamlit run app.py