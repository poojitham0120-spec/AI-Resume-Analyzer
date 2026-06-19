import streamlit as st
from PyPDF2 import PdfReader


# -----------------------------
# Configuration
# -----------------------------

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "mysql",
    "react",
    "node.js",
    "spring boot",
    "machine learning",
    "artificial intelligence",
    "git",
    "github",
    "aws",
    "docker"
]


# -----------------------------
# Utility Functions
# -----------------------------

def extract_resume_text(pdf_file):
    """Extract text from uploaded PDF resume."""

    pdf_reader = PdfReader(pdf_file)
    text = ""

    for page in pdf_reader.pages:
        content = page.extract_text()

        if content:
            text += content

    return text.lower()


def find_skills(resume_text):
    """Find matching skills from resume."""

    found_skills = []

    for skill in SKILLS:
        if skill in resume_text:
            found_skills.append(skill)

    return found_skills


def calculate_resume_score(found_skills):
    """Calculate resume score."""

    return min(len(found_skills) * 8, 100)


def calculate_ats_score(resume_text, found_skills):
    """Calculate ATS compatibility score."""

    score = 0

    if len(resume_text) > 500:
        score += 25

    if len(found_skills) >= 5:
        score += 25

    if "project" in resume_text or "projects" in resume_text:
        score += 25

    if "certification" in resume_text or "certifications" in resume_text:
        score += 25

    return score


def calculate_job_match(resume_text, job_description):
    """Calculate JD matching score."""

    jd_text = job_description.lower()

    matched_skills = 0
    total_jd_skills = 0

    for skill in SKILLS:

        if skill in jd_text:

            total_jd_skills += 1

            if skill in resume_text:
                matched_skills += 1

    if total_jd_skills == 0:
        return 0

    return int((matched_skills / total_jd_skills) * 100)


def find_missing_skills(resume_text, job_description):
    """Find skills missing from resume."""

    jd_text = job_description.lower()

    missing = []

    for skill in SKILLS:

        if skill in jd_text and skill not in resume_text:
            missing.append(skill)

    return missing


def generate_suggestions(
    resume_score,
    ats_score,
    missing_skills
):
    """Generate improvement suggestions."""

    suggestions = []

    if resume_score < 60:
        suggestions.append(
            "Add more technical skills."
        )

    if ats_score < 75:
        suggestions.append(
            "Include projects and certifications."
        )

    if missing_skills:
        suggestions.append(
            "Add missing skills relevant to the job description."
        )

    return suggestions


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #4facfe, #00f2fe);
}

/* Main Title */
h1 {
    color: #ffffff;
    text-align: center;
    font-weight: bold;
}

/* Subheaders */
h2, h3 {
    color: #1B1464;
}

/* Labels */
label {
    color: #000080 !important;
    font-weight: bold;
}

/* Text Area */
textarea {
    background-color: #f5f5f5 !important;
    color: black !important;
    border-radius: 10px !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
}

/* Progress Bars */
.stProgress > div > div > div > div {
    background-color: #00C853;
}

/* Success Message */
.stSuccess {
    background-color: #C8E6C9;
    color: black;
    border-radius: 10px;
}

/* Warning Message */
.stWarning {
    background-color: #FFF3CD;
    color: black;
    border-radius: 10px;
}

/* Info Message */
.stInfo {
    background-color: #BBDEFB;
    color: black;
    border-radius: 10px;
}

/* Buttons */
.stButton>button {
    background-color: #FF9800;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #F57C00;
    color: white;
}

/* Divider */
hr {
    border: 2px solid #1B1464;
}

</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer & ATS Checker")

st.write(
    "Upload a resume and compare it against a job description."
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# -----------------------------
# Processing
# -----------------------------

if uploaded_file:

    resume_text = extract_resume_text(uploaded_file)

    found_skills = find_skills(resume_text)

    resume_score = calculate_resume_score(
        found_skills
    )

    ats_score = calculate_ats_score(
        resume_text,
        found_skills
    )

    st.divider()

    # Skills

    st.subheader("Skills Found")

    if found_skills:
        st.success(", ".join(found_skills))
    else:
        st.warning("No matching skills found.")

    # Resume Score

    st.subheader("Resume Score")

    st.progress(resume_score)

    st.write(
        f"Score: {resume_score}/100"
    )

    # ATS Score

    st.subheader("ATS Compatibility")

    st.progress(ats_score)

    st.write(
        f"ATS Score: {ats_score}/100"
    )

    # Job Description Analysis

    if job_description:

        match_score = calculate_job_match(
            resume_text,
            job_description
        )

        missing_skills = find_missing_skills(
            resume_text,
            job_description
        )

        st.subheader(
            "Job Description Match"
        )

        st.progress(match_score)

        st.write(
            f"Match Score: {match_score}%"
        )

        st.subheader(
            "Missing Skills"
        )

        if missing_skills:
            st.warning(
                ", ".join(missing_skills)
            )
        else:
            st.success(
                "No missing skills detected."
            )

        st.subheader(
            "Suggestions"
        )

        suggestions = generate_suggestions(
            resume_score,
            ats_score,
            missing_skills
        )

        if suggestions:

            for item in suggestions:
                st.write(f"• {item}")

        else:
            st.success(
                "Excellent! Resume looks strong."
            )

    st.subheader(
        "Resume Preview"
    )

    st.text_area(
        "Extracted Text",
        resume_text[:3000],
        height=250
    )