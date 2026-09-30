# BookFit — Explainable Technical Book Recommender

A lightweight MVP that recommends the top 3 technical books from:
- Subject
- Learning level
- Practical/Theoretical preference

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Why this MVP
The ranking is intentionally explainable instead of asking an LLM to invent recommendations. It scores:
- 50% practical/theoretical preference match
- 35% level match
- 15% rating

The small catalog can later be replaced with Goodreads/Google Books metadata and a semantic retrieval layer.

