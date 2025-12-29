# ResumeParser — Job-focused Resume Analyzer

Live demo: [job-based-resume.streamlit.app](https://job-based-resume.streamlit.app/)  
Repository: [Kvmeena12/ResumeParser](https://github.com/Kvmeena12/ResumeParser)

A simple Streamlit app that parses resumes (PDF/DOCX/TXT), compares them to a job description, and produces role-fit scores, highlights, and suggested resume bullet rewrites for applicants and recruiters.

---

## Quick links
- Live demo: [job-based-resume.streamlit.app](https://job-based-resume.streamlit.app/)
- Repo: [github.com/Kvmeena12/ResumeParser](https://github.com/Kvmeena12/ResumeParser)

---

## Features
- Upload a resume (PDF / DOCX / TXT) and paste or upload a job description
- Extract and normalize resume sections (experience, education, skills)
- Compare resume to job description and produce match scores and suggestions
- Streamlit UI with interactive controls and downloadable results (CSV / JSON)

---

## Repository structure (simple)
- `app_ui.py` — Streamlit app entrypoint and UI
- `requirements.txt` — Python dependencies
- `src/`
  - `loaders.py` — resume document loaders and text extraction
  - `jd_loader.py` — job description parsing and normalization
  - `llm.py` — LLM wrapper and prompt orchestration
  - `utils.py` — helper utilities

---

## Installation (local)
1. Clone the repo
   - git clone https://github.com/Kvmeena12/ResumeParser.git
   - cd ResumeParser
2. Create and activate a virtual environment (recommended)
   - python -m venv .venv
   - macOS / Linux: source .venv/bin/activate
   - Windows (PowerShell): .venv\Scripts\Activate.ps1
3. Install dependencies
   - pip install -r requirements.txt
4. Set environment variables (example)
   - `OPENAI_API_KEY` — if using OpenAI in `src/llm.py`
5. Run the app
   - streamlit run app_ui.py
6. Open http://localhost:8501

---

## Deployment (short)
- Streamlit Cloud: Add the repo to Streamlit Cloud, set `requirements.txt` and environment variables (e.g., `OPENAI_API_KEY`).
- Docker: Build a container from a Python base, install requirements, set env vars, and run `streamlit run app_ui.py --server.port $PORT`.

---

## Configuration
- To change LLM provider, update `src/llm.py` with the provider code and required keys.

---

## Quick usage
1. Open the app (local or deployed).
2. Upload a candidate resume (PDF/DOCX/TXT).
3. Paste or upload the job description.
4. Click "Analyze".
5. Review:
   - Role-fit score
   - Section highlights
   - Suggested bullet rewrites

---

## Extending the project
- Swap LLM provider in `src/llm.py`.
- Add embeddings/vector search (Pinecone, Weaviate, FAISS).
- Improve parsing in `src/loaders.py` (e.g., `pdfplumber`, `python-docx`, `unstructured`).
- Add a section classifier for more accurate extraction.

---

## Troubleshooting & tips
- Use Python 3.8+ and ensure `requirements.txt` installed correctly.
- Large inputs may increase cost or timeout LLM calls — summarize long resumes or JDs first.
- If LLM responses vary, add few-shot examples or more prompt instructions.

---

## Contributing
Contributions are welcome:
1. Open an issue describing the change.
2. Fork the repo and create a feature branch.
3. Submit a PR with changes and tests where appropriate.

---

## Contact
Maintained by Kvmeena12. For questions or collaboration, open an issue or visit the GitHub profile.
