import json

def skill_evidence_agent(llm, structured_resume, job_description):
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) Skill Analyst.

    TASK:
    Compare the Job Description with the Resume and evaluate skill match
    based strictly on EVIDENCE, not keyword stuffing.
    
    IMPORTANT RULES:
    - Academic research and projects ARE valid experience
    - Implied skills count as PRESENT
    - Mark a skill MISSING only if it is REQUIRED and has ZERO evidence
    - No extra text, no explanations
    
    OUTPUT LIMITS (VERY IMPORTANT):
    - Experience is also missing skill if not same as JD 
    - Max 6 missing_skills
    - Max 6 strengths
    - Max 6 recommendations
    - Each item max 12 words

    ATS SCORE RULES:
    - Start from 100
    - Deduct ONLY for truly missing REQUIRED skills
    -Deduct 10 if missing skills are greater than equal to 5
    - Do NOT deduct for preferred skills
    - Minimum score: 50 unless resume is clearly unrelated
    - Do NOT easily give score > 85
    - if there is experience reudce ATS Score 
    - Separately evaluate hard skills, tools, and soft skills

    
    RETURN STRICT JSON ONLY.
    JSON FORMAT:
    {{
        "ats_score": number,
        "missing_skills": [],
        "strengths": [],
        "recommendations": []
}}
     RESUME:
     {structured_resume}
     
     JOB DESCRIPTION:
     {job_description}
RETURN JSON ONLY.
"""

    # ---------- SAFE RETRY LOOP ----------
    for attempt in range(2):
        try:
            response = llm.invoke(prompt)

            text = (
                response.content
                if hasattr(response, "content")
                else str(response)
            )

            parsed = json.loads(text)

            # Basic schema safety
            return {
                "ats_score": int(parsed.get("ats_score", 75)),
                "missing_skills": parsed.get("missing_skills", [])[:6],
                "strengths": parsed.get("strengths", [])[:6],
                "recommendations": parsed.get("recommendations", [])[:6],
            }

        except Exception:
            if attempt == 1:
                # HARD FALLBACK — THIS ENSURE APP NEVER CRASHES
                return {
                    "ats_score": 75,
                    "missing_skills": [],
                    "strengths": [],
                    "recommendations": [
                        "Retry analysis for more detailed ATS insights"
                    ],
                }
