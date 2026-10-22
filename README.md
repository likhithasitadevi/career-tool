# 🎯 Student Skill-Gap & Career Roadmap Tool

An AI-powered web app that helps students find the gap between their current skills and the skills needed for their dream tech role, then generates a personalized week-by-week learning plan.

**🔗 Live demo:** https://career-ls.streamlit.app
<img width="1470" height="956" alt="Screenshot 2026-10-22 at 11 13 17 PM copy" src="https://github.com/user-attachments/assets/c5d7e157-0861-4035-8209-f05fcb48bf6d" />




## Features

- **Skill-gap analysis:** pick a target role and tick the skills you already have to see your readiness percentage and missing skills
- **AI resume scanner:** upload a PDF resume and detected skills are ticked automatically
- **AI learning roadmap:** get a custom plan (2 to 12 weeks) with goals, topics, free resources, and mini projects
- **Download:** save your roadmap as a Markdown file
- **Roles covered:** Software Developer, Frontend, Backend, Data Scientist, Data Analyst, Cloud/DevOps Engineer

## Tech stack

- Python
- Streamlit (UI and hosting)
- Groq API (LLM for resume parsing and roadmap generation)
- pypdf (PDF text extraction)

## Run it locally

1. Clone the repo
```bash
   git clone https://github.com/likhithasitadevi/career-tool.git
   cd career-tool
```
2. Install dependencies
```bash
   pip install -r requirements.txt
```
3. Get a free API key from [console.groq.com](https://console.groq.com) and create `.streamlit/secrets.toml`:
```toml
   GROQ_API_KEY = "your_key_here"
```
4. Run the app
```bash
   streamlit run app.py
```

## How it works

1. The role requirements are stored in a Python dictionary, which is easy to extend with new roles and skills.
2. The resume text is extracted with pypdf and sent to an LLM, which returns only the skills from the allowed list.
3. Missing skills and your target role are sent to the LLM to build the roadmap.

## Future improvements

- Add more roles and skills
- Save progress across sessions
- Support scanned (image-based) PDFs with OCR

## Author

YOUR NAME: [LinkedIn](YOUR-LINKEDIN-URL)
