import json
import os

import streamlit as st
from groq import Groq
from pypdf import PdfReader

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
# Tried in order; if one is retired (404 model_not_found) the next is used.
# Check console.groq.com/docs/models occasionally, since Groq retires models often.
MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
MAX_RESUME_CHARS = 12000

st.set_page_config(page_title="Skill-Gap & Career Roadmap Tool", page_icon="🎯", layout="wide")

st.title("🎯 Student Skill-Gap & Career Roadmap Tool")
st.write("Analyze your tech skills, identify gaps for your dream job, and get an AI-powered roadmap.")

# ------------------------------------------------------------------
# Role requirements database (add more roles/skills freely)
# ------------------------------------------------------------------
roles_requirements = {
    "Software Developer": [
        "Python", "JavaScript", "Data Structures & Algorithms", "Databases/SQL",
        "Git", "REST APIs", "Docker", "System Design Basics",
    ],
    "Frontend Developer": [
        "HTML/CSS", "JavaScript", "React", "TypeScript", "Git",
        "Responsive Design", "REST APIs", "Testing",
    ],
    "Backend Developer": [
        "Python/Java/Node.js", "Databases/SQL", "REST APIs", "Authentication",
        "Git", "Docker", "Caching", "System Design Basics",
    ],
    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning", "Pandas",
        "Data Visualization", "Scikit-learn", "Deep Learning Basics",
    ],
    "Data Analyst": [
        "SQL", "Excel", "Python", "Pandas", "Data Visualization",
        "Power BI/Tableau", "Statistics", "Communication",
    ],
    "Cloud/DevOps Engineer": [
        "Linux", "Docker", "Kubernetes", "AWS/Cloud", "Networking",
        "Terraform", "CI/CD", "Git",
    ],
}


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def checkbox_key(role: str, skill: str) -> str:
    return f"skill_{role}_{skill}"


HARDCODED_API_KEY = ""  # Optional: paste "gsk_..." here ONLY if your GitHub repo is PRIVATE


def get_api_key() -> str:
    """Key comes from the code, Streamlit secrets, or an environment variable.
    Visitors never see or enter it."""
    if HARDCODED_API_KEY:
        return HARDCODED_API_KEY
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")


def ask_llm(prompt: str, temperature: float = 0.5):
    """Call Groq and return text, or None after showing an error."""
    api_key = get_api_key()
    if not api_key:
        st.error("The AI service isn't configured yet. Please try again later.")
        return None
    client = Groq(api_key=api_key)
    last_error = None
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            if "model_not_found" in str(e) or "404" in str(e):
                continue  # try the next model
            break  # other errors (bad key, rate limit) won't be fixed by another model
    st.error(f"Groq API error: {last_error}")
    return None


def parse_json_list(text: str):
    """Pull a JSON list out of a model reply, even if it adds extra words."""
    try:
        start, end = text.index("["), text.rindex("]") + 1
        data = json.loads(text[start:end])
        return [str(x) for x in data] if isinstance(data, list) else []
    except (ValueError, json.JSONDecodeError):
        return []


# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tab1, tab2 = st.tabs(["📊 Skill Gap & Roadmap Generator", "📄 AI Resume Scanner"])

# NOTE: the resume tab is written FIRST on purpose. Streamlit does not allow
# changing a widget's state after the widget is drawn, so the scanner must run
# before the checkboxes in tab1 are created. The visual tab order is unchanged.

# ---------------------------- TAB 2: Resume scanner ----------------------------
with tab2:
    st.subheader("Smart AI Resume Ingestion")
    st.write("Upload your resume PDF. Detected skills will be auto-ticked in the first tab.")

    uploaded_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"])

    if uploaded_pdf and st.button("Scan Resume with AI"):
        with st.spinner("Extracting text and analyzing skills..."):
            try:
                reader = PdfReader(uploaded_pdf)
                resume_text = "".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                st.error(f"Could not read this PDF: {e}")
                resume_text = ""

            if not resume_text.strip():
                st.error("Couldn't read text from this PDF (it may be a scanned image).")
            else:
                all_skills = sorted({s for skills in roles_requirements.values() for s in skills})
                prompt = f"""You are a resume parser.
From the resume below, return ONLY a JSON array of skills from this allowed list
that the candidate clearly has evidence of (projects, experience, skills section).
Do not add skills outside the list. No explanation, no markdown.

Allowed list: {json.dumps(all_skills)}

Resume:
{resume_text[:MAX_RESUME_CHARS]}"""

                reply = ask_llm(prompt, temperature=0)
                if reply is not None:
                    found = parse_json_list(reply)
                    found_lower = {f.lower() for f in found}
                    matched = []
                    for role, skills in roles_requirements.items():
                        for skill in skills:
                            if skill.lower() in found_lower:
                                st.session_state[checkbox_key(role, skill)] = True
                                matched.append(skill)
                    if matched:
                        st.success(
                            f"Detected {len(set(matched))} skills: "
                            f"{', '.join(sorted(set(matched)))}. "
                            "Switch to the first tab to see them ticked."
                        )
                    else:
                        st.warning("No matching skills detected. Tick them manually in the first tab.")
    elif uploaded_pdf is None:
        st.info("Upload a PDF to begin.")

# ---------------------------- TAB 1: Skill gap ----------------------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Select Target Role")
        target_role = st.selectbox("Dream Career Role:", list(roles_requirements.keys()))
        required_skills = roles_requirements[target_role]

        st.subheader("2. Check Your Current Skills")
        user_skills = []
        for skill in required_skills:
            if st.checkbox(skill, key=checkbox_key(target_role, skill)):
                user_skills.append(skill)

    # Computed live, so results never disappear when other buttons are clicked
    missing_skills = [s for s in required_skills if s not in user_skills]
    match_percentage = int(len(user_skills) / len(required_skills) * 100)

    with col2:
        st.subheader("3. Results & Gap Analysis")
        st.metric(label="Role Readiness Match", value=f"{match_percentage}%")
        st.progress(match_percentage / 100)

        if missing_skills:
            st.warning(f"**Identified Skill Gaps:** {', '.join(missing_skills)}")
        else:
            st.success("Congratulations! You possess all core requirements listed for this role.")

    st.divider()

    # ---------------------------- AI roadmap ----------------------------
    st.subheader("4. AI Learning Roadmap")
    weeks = st.slider("Plan length (weeks)", 2, 12, 4)

    if st.button("Generate AI Learning Roadmap"):
        with st.spinner("Building your customized learning milestones..."):
            focus = ", ".join(missing_skills) if missing_skills else "None, focus on advanced portfolio projects"
            prompt = f"""Create a practical {weeks}-week structured learning plan and milestone checklist
for a student targeting the role of {target_role}.
Skills they already have: {', '.join(user_skills) if user_skills else 'None yet'}.
Their missing skills are: {focus}.
For each week give: goals, study topics, free resources to use, and a hands-on mini project.
End with one portfolio project idea that combines the skills. Keep it clear and concise, in markdown."""
            text = ask_llm(prompt)
            if text:
                st.session_state["roadmap"] = {"role": target_role, "text": text}

    roadmap = st.session_state.get("roadmap")
    if roadmap:
        st.subheader(f"🗺️ Custom Roadmap for {roadmap['role']}")
        st.markdown(roadmap["text"])
        st.download_button(
            "Download roadmap (.md)",
            data=roadmap["text"],
            file_name=f"{roadmap['role'].replace('/', '-').replace(' ', '_')}_roadmap.md",
            mime="text/markdown",
        )
