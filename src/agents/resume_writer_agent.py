import json
import re


def _extract_json_safely(text: str):
    """
    Extracts the FIRST valid JSON object from text.
    Handles partial / noisy generations.
    """
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try regex-based JSON extraction
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    return None


def resume_writer_agent(llm, structured_resume, job_description):
    prompt = f"""
    You are an ATS Senior resume writer.
    Rewrite the resume using the PROVIDED STRUCTURE ONLY.
    DO NOT add new roles, projects, or research.
    DO NOT move items between sections.
    For the Experience write at least 3-4 lines ,2-3 lines for project, and for research 4-5 lines in simple language.
    Improve:
    - Bullet points quality
    - Add ATS keywords
    - Clarity
    - According to job role
    Return JSON with SAME structure and keys.
    
    Structured Resume: {json.dumps(structured_resume, indent=2)}
    Job Description: {job_description}
"""

    last_error = None

    # Retry logic (important for Groq stability)
    for attempt in range(3):
        try:
            response = llm.invoke(prompt)
            text = response.content if hasattr(response, "content") else str(response)

            parsed = _extract_json_safely(text)

            if isinstance(parsed, dict):
                return parsed

            last_error = "Invalid JSON structure"

        except Exception as e:
            last_error = str(e)

    # HARD FALLBACK — NEVER CRASH UI
    print(f"[resume_writer_agent] Failed after retries: {last_error}")
    return structured_resume
