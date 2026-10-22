# 🎯 Student Skill-Gap & Career Roadmap Tool

An AI-powered web app that helps students find the gap between their current skills and the skills needed for their dream tech role, then generates a personalized week-by-week learning plan.

**🔗 Live demo:** https://career-ls.streamlit.app

<img width="600" alt="Screenshot 2026-10-22 at 11 21 48 PM" src="https://github.com/user-attachments/assets/c45a0368-c38d-4968-a4c2-9bb6de5e0048" />
<img width="600" alt="Screenshot 2026-10-22 at 11 21 56 PM" src="https://github.com/user-attachments/assets/d8a18071-1aeb-4ad1-80dc-824655cb5a91" />
<img width="600" alt="Screenshot 2026-10-22 at 11 22 03 PM" src="https://github.com/user-attachments/assets/3b659ea8-7c6c-4ba3-ab33-42924f2482c2" />


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

Likhitha : https://www.linkedin.com/in/likhitha-yelubandi-698759374/
