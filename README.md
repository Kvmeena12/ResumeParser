# ResumeParser — Job-based Resume Analyzer & Matching
Live demo: [job-based-resume.streamlit.app](https://job-based-resume.streamlit.app/)

A Streamlit-powered resume parsing and job-matching assistant that analyzes uploaded resumes against job descriptions and produces a job-focused, ranked summary for applicants and recruiters. This repository contains the Streamlit UI and the core parsing/LLM integration.

## Quick links
- Live demo: https://job-based-resume.streamlit.app/
- Repo: https://github.com/Kvmeena12/ResumeParser

---

## Features
- Upload a resume (PDF/DOCX/TXT) and a job description (paste or upload)
- Extract resume content and normalize sections (experience, education, skills)
- Compare resume content to a job description and produce job-specific scoring or suggestions
- Streamlit UI with interactive controls and downloadable results

---

## Repository structure and model design

Top-level files
- `app_ui.py` — Streamlit application entrypoint and UI logic. Handles file upload, job description input, displays results and controls the flow from input → processing → output.
- `requirements.txt` — Python dependencies required to run the app.

src/ (core logic)
- `src/loaders.py` — Document loader utilities. This module is responsible for reading uploaded files, extracting text from different formats (PDF, DOCX, TXT), and returning normalized text blocks or sections.
- `src/jd_loader.py` — Job Description loader utilities. Focuses on ingesting job descriptions, cleaning and structuring job responsibilities, skills, and requirements.
- `src/llm.py` — LLM wrapper and prompt orchestration. Encapsulates calls to your chosen language model (for example OpenAI or other LLM endpoint), manages prompts, and post-processes model outputs into structured JSON or scores.
- `src/utils.py` — Shared helper functions and small utilities used across modules (parsing helpers, text clean-up, scoring utilities).

Dev environment
- `.devcontainer/` — Optional devcontainer configuration for reproducible development inside VS Code Remote Containers.

Data & flow (overview)
1. User uploads a resume and enters/pastes a job description in the Streamlit UI.
2. `app_ui.py` sends the uploaded file to `src/loaders.py` which extracts and normalizes the resume text.
3. Job description is processed by `src/jd_loader.py` to extract key responsibilities, required skills, and seniority information.
4. `src/llm.py` receives normalized resume text + structured job description and:
   - runs the analysis prompt (match scoring, rewrite suggestions, role-fit summary)
   - extracts structured outputs (scores, highlights, suggested resume changes)
5. Results are rendered in the Streamlit UI and can be downloaded or copied.

Note: The code separates concerns so you can easily swap the LLM provider, add embeddings/vector search, or connect an external database/vector store later.

---

## Installation (local)

1. Clone the repository
   git clone https://github.com/Kvmeena12/ResumeParser.git
   cd ResumeParser

2. Create a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Set environment variables (example)
   - `OPENAI_API_KEY` — if you use OpenAI via `src/llm.py`.
   - Any other credentials your LLM or vector DB requires (the repo will indicate specifics if added).

5. Run the Streamlit app
   streamlit run app_ui.py

Open http://localhost:8501 in your browser to view the UI.

---

## Deployment (Streamlit Cloud / Heroku / Docker)

Streamlit Cloud (recommended for demos)
- Add this repo to Streamlit Cloud and set the `requirements.txt` and any environment variables (e.g., `OPENAI_API_KEY`) in the Streamlit app settings.
- The live app is available at: https://job-based-resume.streamlit.app/

Docker (production)
- Create a Dockerfile wrapping a Python base image, copy the repo, install requirements, set env vars, and run `streamlit run app_ui.py --server.port $PORT`.
- Expose and bind your port as needed and use a production-ready reverse proxy for TLS.

Notes on secret management
- Never store API keys in the repo. Use environment variables or secrets management offered by hosting platforms (Streamlit Cloud secrets, GitHub Actions secrets, etc.).

---

## Usage examples

Example 1 — Quick match
1. Upload a resume PDF in the UI.
2. Paste a job description into the Job Description box.
3. Click Analyze.
4. The UI will show:
   - A role-fit score
   - Section-by-section highlights
   - Suggested resume bullet rewrites to better match the job

Example 2 — Downloading suggestions
- After analysis, use the download button to export the suggestions and modified resume bullets as a CSV or JSON.

---

## Extending the model

Swap LLM provider
- Modify `src/llm.py` to use another provider (Anthropic, Hugging Face inference, local LLM) while keeping prompt format stable.

Add embeddings & vector search
- Pre-compute embeddings for job descriptions and candidate experiences to enable semantic matching with a vectordb (Pinecone, Weaviate, FAISS).
- Store embeddings and add a nearest-neighbor match step before or after LLM analysis to surface similar experiences.

Add more robust parsing
- Improve `src/loaders.py` by integrating `unstructured`, `pdfplumber` or `python-docx` for better structure extraction.
- Add a section classifier to identify experience, education, skills, and projects more reliably.

---

## Troubleshooting & tips

- If the app fails to start, check your Python version (3.8+ recommended) and that `requirements.txt` packages installed correctly.
- For long resumes or large job descriptions, model calls may timeout or cost more; consider summarizing long inputs before sending to the LLM.
- If using OpenAI: validate your API key and quota. If responses are inconsistent, add more in-prompt examples or apply few-shot templates.

---

## Security & Privacy
- Resumes often contain personal data. If deploying publicly, ensure secure transport (HTTPS), and implement data deletion policies and user consent notices.
- For production, avoid logging full resume text and rotate API keys regularly.

---

## Contribution
Contributions, issues and feature requests are welcome. Steps:
1. Open an issue describing the change or improvement.
2. Fork the repo and create a feature branch.
3. Submit a PR — include tests where appropriate.

---

## License
Specify your license here (e.g., MIT). Add a LICENSE file to the repo if you haven’t already.

---

## Contact
Created and maintained by Kvmeena12. For questions or partnership, open an issue or reach via GitHub profile.
