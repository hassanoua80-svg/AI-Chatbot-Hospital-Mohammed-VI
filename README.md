# HUIM6 Learning Assistant — Student AI Chatbot

## Overview
Educational Python + Streamlit chatbot that answers administrative questions using the supplied local JSON knowledge file.

## Run on Windows
1. Extract the ZIP and open this folder in VS Code.
2. Open Terminal > New Terminal.
3. Run `python -m venv .venv`
4. Activate it: `.venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Start the app: `streamlit run app.py`
7. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Files
- `app.py`: Streamlit interface and answer matching
- `Hospital-Mohammed-VI-knowledge.json`: supplied knowledge base
- `requirements.txt`: Python dependency
- `Rapport_Projet_Chatbot_IA.docx`: French project report

## Limitations
This is a keyword/FAQ matching prototype, not a trained generative AI model or a live hospital system. It cannot book appointments or confirm live availability and must not provide clinical advice. Never enter sensitive personal data.
