# 🎯 Student Skill-Gap & Career Roadmap Tool

An AI-powered web app that helps students find the gap between their current skills and the skills needed for their dream tech role, then generates a personalized week-by-week learning plan.

**🔗 Live demo:** https://career-ls.streamlit.app

<img width="500" alt="Screenshot 2026-10-22 at 11 49 36 PM" src="https://github.com/user-attachments/assets/95bb079e-8337-4dba-878c-cdd4561a655f" />
<img width="500" alt="Screenshot 2026-10-22 at 11 49 44 PM" src="https://github.com/user-attachments/assets/c0d4570f-af6a-4729-b970-00d47073d9ff" />
<img width="500" alt="Screenshot 2026-10-22 at 11 49 52 PM" src="https://github.com/user-attachments/assets/181622ea-f730-4a56-9d79-392dcd2975ac" />


## Features

- **Skill-gap analysis:** pick a target role and tick the skills you already have to see your readiness percentage and missing skills
- **AI resume scanner:** upload your resume and detected skills are ticked automatically
  - Supports **PDF, Word (.docx), plain text (.txt)** and **images (PNG/JPG)**
  - Images are read directly by a vision model, so even a screenshot or photo of a resume works
- **AI learning roadmap:** get a custom plan (2 to 12 weeks) with goals, topics, free resources, and mini projects
- **Download:** save your roadmap as a Markdown file
- **Roles covered:** Software Developer, Frontend, Backend, Data Scientist, Data Analyst, Cloud/DevOps Engineer

## Tech stack

- Python
- Streamlit (UI and hosting)
- Groq API (LLM for resume parsing and roadmap generation, plus a vision model for image resumes)
- pypdf (PDF text extraction)
- python-docx (Word document extraction)

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

1. Role requirements are stored in a Python dictionary, which is easy to extend with new roles and skills.
2. For PDF, DOCX and TXT resumes, the text is extracted locally and sent to an LLM, which returns only skills from the allowed list.
3. For image resumes, the picture is sent to a vision-capable model that reads it and returns the matching skills.
4. Missing skills and the target role are sent to the LLM to build the learning roadmap.

## Notes

- The app uses Groq's free tier, so heavy use may hit rate limits.
- Model names on Groq change from time to time. If something stops working, update the `MODELS` and `VISION_MODELS` lists at the top of `app.py`.
- Old `.doc` files are not supported. Please save as `.docx` or PDF.

## Future improvements

- Add more roles and skills
- Save progress across sessions
- Support multiple resumes at once

## Author

Likhitha : https://www.linkedin.com/in/likhitha-yelubandi-698759374/
