import streamlit as st
import os
import json



from src.loaders import load_resume
from src.utils import clean_text
from src.llm import load_llm

from src.agents.structuring_agent import structuring_agent
from src.agents.skill_evidence_agent import skill_evidence_agent
from src.agents.resume_writer_agent import resume_writer_agent
from src.agents.summary_agent import summary_agent


st.set_page_config(
    page_title="AI Resume Intelligence System",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(56,189,248,0.08), transparent 40%),
        radial-gradient(circle at 25% 25%, rgba(168,85,247,0.08), transparent 45%),
        radial-gradient(circle at 50% 85%, rgba(14,165,233,0.06), transparent 50%),
        linear-gradient(180deg, #020617 0%, #020617 100%);
    background-attachment: fixed;
    color: #e5e7eb;
    font-family: Inter, sans-serif;
}


</style>

""", unsafe_allow_html=True)
st.markdown("""
<style>
.skill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 6px;
}

.skill-pill {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
}

.skill-missing {
    background: rgba(239,68,68,0.15);
    color: #fecaca;
    border: 1px solid rgba(239,68,68,0.35);
}

.skill-matched {
    background: rgba(34,197,94,0.15);
    color: #bbf7d0;
    border: 1px solid rgba(34,197,94,0.35);
}
</style>
""", unsafe_allow_html=True)

def extract_summary(summary_output):
    """
    Ensures summary is always clean readable text
    """
    if isinstance(summary_output, dict):
        return summary_output.get("summary", "")

    if isinstance(summary_output, str):
        try:
            parsed = json.loads(summary_output)
            if isinstance(parsed, dict):
                return parsed.get("summary", summary_output)
        except json.JSONDecodeError:
            return summary_output

    return ""



st.markdown("""
<style>
.hero {
    padding: 60px 40px 30px 40px;
}
.hero-title {
    font-size: 44px;
    font-weight: 800;
    color: white;
}
.hero-rotator {
    height: 42px;
    overflow: hidden;
    margin-top: 10px;
}

.hero-rotator-inner {
    display: flex;
    flex-direction: column;
    animation: slideUp 25s infinite;
}

.hero-line {
    height: 42px;
    font-size: 28px;
    font-weight: 700;
    display: flex;
    align-items: center;
}
.hero-line:nth-child(1) { color: #38bdf8; }
.hero-line:nth-child(2) { color: #22c55e; }
.hero-line:nth-child(3) { color: #f59e0b; }
.hero-line:nth-child(4) { color: #a78bfa; }
.hero-line:nth-child(5) { color: #34d399; }

@keyframes slideUp {
    0%   { transform: translateY(0); }
    20%  { transform: translateY(0); }

    25%  { transform: translateY(-42px); }
    40%  { transform: translateY(-42px); }

    45%  { transform: translateY(-84px); }
    60%  { transform: translateY(-84px); }

    65%  { transform: translateY(-126px); }
    80%  { transform: translateY(-126px); }

    85%  { transform: translateY(-168px); }
    100% { transform: translateY(-168px); }
}
.hero-tagline {
    margin-top: 10px;
    font-size: 15px;
    color: #94a3b8;
}
.glass {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}
[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #22c55e;
}

.stTabs [data-baseweb="tab"] {
    font-size: 15px;
    color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom: 2px solid #38bdf8;
}

.footer {
    margin-top: 40px;
    padding: 16px;
    text-align: center;
    font-size: 13px;
    color: #94a3b8;
    border-top: 1px solid #1e293b;
}

.footer a {
    color: #38bdf8;
    text-decoration: none;
    margin: 0 8px;
}
.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #22c55e);
    color: #020617;
    font-weight: 700;
    border-radius: 12px;
    padding: 12px;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #22c55e, #38bdf8);
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
  <div class="hero-container">
  <div class="hero-title">A smarter way to</div>

  <div class="hero-rotator">
    <div class="hero-rotator-inner">
      <div class="hero-line">analyze resumes with real evidence</div>
      <div class="hero-line">understand what recruiters actually see</div>
      <div class="hero-line">validate skills from real work</div>
      <div class="hero-line">get honest, clear resume feedback</div>
      <div class="hero-line">avoid inflated or fake experience</div>
    </div>
  </div>

  <div class="hero-tagline">
    Built on evidence • Clear insights • No guesswork
  </div>
</div>

""", unsafe_allow_html=True)

st.divider()


uploaded_resume = st.file_uploader(
    "Upload Resume (PDF / DOCX)",
    type=["pdf", "docx"]
)

jd_text = st.text_area(
    "Paste Job Description",
    height=260,
    placeholder="Paste the full job description here..."
)

analyze_clicked = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=False
)


def safe_join(items):
    return " | ".join([i for i in items if i])


def render_experience(items):
    for e in items:
        with st.expander(
            safe_join([e.get("position"), e.get("company"), e.get("dates")]) 
            or "Experience"
        ):
            descriptions = e.get("description", [])
            
            if isinstance(descriptions, list):
                for point in descriptions:
                    st.markdown(f"• {point}")
            else:
                st.write(descriptions)


def normalize_to_list(value):
    """
    Converts list / dict / string into a clean list of strings
    """
    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        # sort numeric keys just in case
        return [value[k] for k in sorted(value.keys(), key=lambda x: int(x))]

    if isinstance(value, str):
        return [value]

    return []

def render_research(items):
    for r in items:
        with st.expander(r.get("title", "Research Work")):

            meta = safe_join([r.get("institution"), r.get("dates")])
            if meta:
                st.markdown(f"**{meta}**")

            if r.get("supervisors"):
                st.markdown(f"**Supervisors:** {r['supervisors']}")

            descriptions = normalize_to_list(r.get("description"))

            for point in descriptions:
                st.markdown(f"• {point}")




def render_projects(items):
    for p in items:
        with st.expander(p.get("title", "Project")):
            desc = p.get("description", [])

            # convert dict → list
            if isinstance(desc, dict):
                desc = [desc[k] for k in sorted(desc.keys())]

            # convert string → list
            if isinstance(desc, str):
                desc = [desc]

            for line in desc:
                st.write(f"- {line}")




if uploaded_resume and jd_text.strip():

    with st.spinner("🔍 Analyzing resume with AI agents..."):

        ext = os.path.splitext(uploaded_resume.name)[1]
        temp_path = f"temp_resume{ext}"

        with open(temp_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())

        resume_text = clean_text(load_resume(temp_path))
        llm = load_llm()


        structured = structuring_agent(llm, resume_text)
        analysis = skill_evidence_agent(llm, structured, jd_text)
        rewritten = resume_writer_agent(llm, structured, jd_text)
        summary_raw = summary_agent(structured, jd_text)
        summary_text = extract_summary(summary_raw)

    st.success("✅ Analysis complete")

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("## 🧠 Resume Analysis")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.metric("ATS Match Score", f"{analysis.get('ats_score', 0)} / 100")

    with c2:
        st.markdown("### ❌ Missing Skills")
        missing = analysis.get("missing_skills", [])
        if missing:
            missing_html = "".join(
            f"<span class='skill-pill skill-missing'>{m}</span>"
            for m in missing
        )
            st.markdown(
            f"<div class='skill-row'>{missing_html}</div>",
            unsafe_allow_html=True
        )
        else:
            st.success("No critical skill gaps detected")

    st.markdown("### ✅ Matched Skills")
    matched = analysis.get("strengths", [])

    if matched:
        matched_html = "".join(
            f"<span class='skill-pill skill-matched'>{s}</span>"
            for s in matched
        )
        st.markdown(
            f"<div class='skill-row'>{matched_html}</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("No matched skills detected")

   

    st.markdown("### ✅ Recommendations")
    for r in analysis.get("recommendations", []):
        st.write(f"• {r}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## 📄 Resume Tailored for This Job")

    tabs = st.tabs(
        ["Summary", "Skills", "Experience", "Research", "Projects"]
    )

    with tabs[0]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.write(summary_text or "Summary not generated.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.write(", ".join(rewritten.get("skills", [])) or "No skills listed.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        render_experience(rewritten.get("experience", []))

    with tabs[3]:
        render_research(rewritten.get("research", []))

    with tabs[4]:
        render_projects(rewritten.get("projects", []))

st.markdown("""
<div class="footer">
© 2025 <b>Kunjbihari</b> • 
<a href="https://github.com/your-github" target="_blank">GitHub</a> •
<a href="https://linkedin.com/in/your-linkedin" target="_blank">LinkedIn</a><br>

Contact: <a href="mailto:Kunj07382@gmail.com">Kunj07382@gmail.com</a><br><br>

Built on real evidence • Safe for research • No made-up experience<br><br>

<span style="font-size:12px; color:#f87171;">
<b>Note:</b> Occasionally, AI processing may face temporary issues.  
If you notice any errors, please re-upload your resume and try again.
</span>
</div>
""", unsafe_allow_html=True)

