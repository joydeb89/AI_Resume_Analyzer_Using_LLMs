# AI_Resume_Analyzer_Using_LLMs
AI_Resume_Analyzer_Using_LLMs
# 🧠 AI Resume Analyzer with Job Description Matching

This project is a Flask-based web application that allows users to:

✅ Upload their resume (.pdf or .docx)  
✅ Paste a job description  
✅ Automatically analyze how well the resume matches the job  
✅ View extracted details (name, email, skills, projects, internships, etc.)  
✅ Store analysis in a database for future reference

---

## 🔧 Tech Stack

- Python 3.9+
- Flask (backend)
- SQLite (database)
- HTML, CSS, JS (frontend)
- PyMuPDF (`fitz`), docx2txt (resume parser)
- Sentence Transformers + KeyBERT (semantic similarity)


---

## 🚀 Getting Started Locally

### 1. Clone the Repository


git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
2. Set Up Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate  # Mac/Linux
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the App
bash
Copy
Edit
python app.py
Visit in browser: http://127.0.0.1:5000

💡 How It Works (In Short)
Upload resume (.pdf or .docx)

Paste job description

The app:

Extracts resume text

Compares with job description

Shows match score

Displays extracted sections like name, email, education, experience

Saves results to the database for logged-in users

🛡 Environment Variables (Optional)
If you're using python-dotenv, create a .env file like this:

env
Copy
Edit
FLASK_SECRET=your-secret-key
And use it in app.py:

python
Copy
Edit
from dotenv import load_dotenv
load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET")

🧠 Future Improvements
Use LLMs for deeper understanding of resumes

Add admin dashboard to view all analyses

Export resume matches as PDF

Integrate email alerts


👨‍💻 Author
Joydeb Pal
GitHub: joydeb89

📄 License
This project is licensed under the MIT License.
