import json
import re


def _safe_json_extract(text: str):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    return None


def _chunk_text(text, max_chars=3000):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + max_chars])
        start += max_chars
    return chunks


def structuring_agent(llm, resume_text):
    """
    STRUCTURING AGENT (ROBUST)
    - Chunks resume
    - Retries
    - Never crashes UI
    """

    resume_chunks = _chunk_text(resume_text)

    combined_structure = {
        "skills": [],
        "experience": [],
        "research": [],
        "projects": [],
        "education": []
    }

    for chunk in resume_chunks:
        prompt = f"""
You are an expert resume parser.

Convert the resume text into STRUCTURED JSON.

RULES (VERY IMPORTANT):
- EXPERIENCE = paid roles / internships / company roles ONLY
- RESEARCH = papers, publications, professors, journals, labs
- PROJECTS = academic / self / course projects ONLY / Open source
- DO NOT duplicate the same item in multiple sections
- DO NOT invent or infer missing data
- If unsure → leave field empty ""
- Output VALID JSON ONLY, no markdown
- If There is a research paper under one/two/more professor you can't say XYZ College Researcher. You can say Author of paper.


{{
  "skills": [],
  "experience": [],
  "research": [],
  "projects": [],
  "education": []
}}

Resume text:
{chunk}
"""

        for attempt in range(2):
            try:
                response = llm.invoke(prompt)
                text = response.content if hasattr(response, "content") else str(response)

                parsed = _safe_json_extract(text)
                if isinstance(parsed, dict):
                    for key in combined_structure:
                        if key in parsed and isinstance(parsed[key], list):
                            combined_structure[key].extend(parsed[key])
                    break

            except Exception:
                continue

    return combined_structure
