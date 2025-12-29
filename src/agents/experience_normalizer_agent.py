import json

def resume_writer_agent(llm, structured_resume, job_description):
  prompt = f"""
You are an expert resume writer.
Rewrite the resume for the job description where candidate gets more interview calls.
CRITICAL RULES:
- NEVER move research into experience
- NEVER merge roles
- Research or publication stays in research 
- Experience = industry / internship only
- Projects remain projects
- Use metrics where available
- DO NOT invent data

Return STRICT JSON ONLY:
{{
  "summary": "string",
  "skills": [strings],
  "experience": [
    {{
      "position": "string",
      "company": "string",
      "dates": "string",
      "description": "string"
    }}
  ],
  "research": [
    {{
      "title": "string",
      "institution": "string",
      "dates": "string",
      "supervisors": "string",
      "description": "string"
    }}
  ],
  "projects": [
    {{
      "title": "string",
      "description": "string"
    }}
  ],
  "education": [
    {{
      "degree": "string",
      "institution": "string",
      "dates": "string"
    }}
  ]
}}

Structured Resume:
{json.dumps(structured_resume)}

Job Description:
{job_description}
"""
  response = llm.invoke(prompt)
  text = response.content if hasattr(response, "content") else str(response)

  try:
    out = json.loads(text)
  except Exception:
      return structured_resume

  #  FINAL SAFETY 
  out["experience"] = structured_resume["experience"]
  out["research"] = structured_resume["research"]

  return out
