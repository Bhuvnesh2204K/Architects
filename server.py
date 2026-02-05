"""
AI Assistant server using Flask + Groq API.
Run: pip install -r requirements-server.txt && python server.py
Then the Portfolio app (Spring Boot) proxies chat to POST http://localhost:5000/api/chat
"""

import json
import os
import sys

# Load .env if present (pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import Flask, request, jsonify
from flask_cors import CORS

# Groq API key: from env/.env or fallback below (get one at https://console.groq.com/keys)
GROQ_API_KEY = (os.environ.get("GROQ_API_KEY") or "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").strip()

if not GROQ_API_KEY or not GROQ_API_KEY.startswith("gsk_"):
    print("ERROR: GROQ_API_KEY is not set or invalid.", file=sys.stderr)
    print("  1. Get a key at https://console.groq.com/keys", file=sys.stderr)
    print("  2. Set it: set GROQ_API_KEY=gsk_your_key_here  (Windows) or export GROQ_API_KEY=gsk_... (Linux/Mac)", file=sys.stderr)
    print("  Or create a .env file in this folder with: GROQ_API_KEY=gsk_your_key_here", file=sys.stderr)
    sys.exit(1)

from groq import Groq

app = Flask(__name__)
# Allow frontend on any localhost port (8080, 8081, 8082, etc.)
CORS(app, origins=[
    "http://localhost:8080", "http://localhost:8081", "http://localhost:8082",
    "http://127.0.0.1:8080", "http://127.0.0.1:8081", "http://127.0.0.1:8082",
], supports_credentials=False)

client = Groq(api_key=GROQ_API_KEY)

DEFAULT_MODEL = "llama-3.1-8b-instant"

FINANCE_SYSTEM_PROMPT = """You are a knowledgeable and professional financial assistant. Your role is to help users with all finance-related questions. Give detailed, thorough answers about:

- Investing: stocks, mutual funds, ETFs, bonds, gold, real estate, and other assets
- Portfolio management: diversification, risk, asset allocation, rebalancing
- Personal finance: budgeting, saving, emergency funds, debt management
- Taxes: capital gains, tax-saving instruments (e.g. ELSS, PPF), TDS, filing
- Markets: how stock markets work, indices (Nifty, Sensex), market hours, order types
- Retirement and goal-based planning: SIPs, lump sum, compounding, inflation
- Insurance and contingency planning where relevant to finance

Answer in detail: include step-by-step explanations, examples where helpful, pros and cons when relevant, and enough context so the user fully understands. Use simple language and explain any jargon. Structure longer answers with short paragraphs or bullet points for readability. If a question is outside finance, you may briefly answer but steer back to finance where useful. Do not give personalized investment advice (e.g. "buy X"); instead explain concepts and options. For regulations or tax rules, mention that laws vary by country/region and suggest consulting a professional when appropriate."""


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ai-assistant"})


@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.get_json(force=True, silent=True)
        if data is None and request.data:
            try:
                data = json.loads(request.data.decode("utf-8"))
            except Exception:
                data = {}
        data = data or {}
        message = (data.get("message") or data.get("msg") or "").strip()
        if not message:
            return jsonify({"error": "Please type a message in the chat box and try again."}), 400

        completion = client.chat.completions.create(
            model=data.get("model") or DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": FINANCE_SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            max_tokens=2048,
            temperature=0.3,
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("AI Assistant (Flask + Groq) starting on http://0.0.0.0:5000")
    print("Ensure Portfolio app is configured with ai.assistant.url=http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)