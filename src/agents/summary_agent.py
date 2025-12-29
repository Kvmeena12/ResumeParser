import json
from src.llm import load_text_llm

def summary_agent(structured_resume: dict, job_description: str) -> str:
    llm_draft = load_text_llm(
        model="llama-3.1-8b-instant",
        temperature=0.5,      # human but controlled
        max_tokens=220        # summary never needs more
    )

    llm_refine = load_text_llm(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.3,
        max_tokens=260
    )

    resume_text = json.dumps(structured_resume, indent=2)

    draft_prompt = f"""
    Write a professional resume summary in 3–4 lines with your Experience that what points in resume hit the hiring manager/Hr.
    Rules:
    - Use ONLY resume facts
    - Align with the job description
    -Simple, clear English, easy english
    - No exaggeration
    - No JSON
    - No bullet points
    - Always Use English Language

    Resume:{resume_text}
    """
    draft = llm_draft.invoke(draft_prompt).content.strip()

    refine_prompt = f"""
    Refine the following resume summary.
    Goals:
    - Improve flow and readability
    - Keep professional tone
    - ATS-friendly but natural
    - No new claims
    - Optimize it for higher chance of interview calls
    
    Summary:{draft}
    
    Job Description: {job_description}
    """
    final_summary = llm_refine.invoke(refine_prompt).content.strip()

    return final_summary
