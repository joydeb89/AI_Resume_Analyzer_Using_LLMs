from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

from backend.parser import parse_resume, parse_job_description
from backend.matcher import analyze_resume_job_match
from backend.extractor import extract_resume_details

# Save analysis to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Get user ID from DB using session user name
cursor.execute("SELECT id FROM users WHERE name = ?", (session['user'],))
user = cursor.fetchone()
if user:
    user_id = user[0]
    cursor.execute('''
        INSERT INTO resume_analysis (user_id, match_score, resume_text, job_description)
        VALUES (?, ?, ?, ?)
    ''', (user_id, result['match_score'], resume_text, jobDesc))
    conn.commit()

conn.close()


app = Flask(__name__)
app.secret_key = 'secret123'

# === DATABASE SETUP ===
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # ✅ Create resume_analysis table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            match_score REAL,
            resume_text TEXT,
            job_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


# === ROUTES ===

@app.route('/')
def home():
    return redirect('/signup')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                           (name, email, password))
            conn.commit()
            flash("Account created successfully!", "success")
        except sqlite3.IntegrityError:
            flash("Email already exists.", "error")
        conn.close()
        return redirect('/signup')
    return render_template('signup.html')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]
            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", "error")
    return render_template('Login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/Login')
    
    result = None          
    details = None  

    if request.method == 'POST':
        resume = request.files['resume']
        jobDesc = request.form['jobDesc']

        if not resume or not jobDesc:
            flash("Please upload resume and paste job description", "error")
            return redirect('/dashboard')

        # Save uploaded file temporarily
        filename = secure_filename(resume.filename)
        upload_dir = 'temp_uploads'
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        resume.save(file_path)

        try:
            resume_text = parse_resume(file_path)
            jd_text = parse_job_description(jobDesc)

            result = analyze_resume_job_match(resume_text, jd_text)
            details = extract_resume_details(resume_text)  # ✅ extract name, email, phone etc.
            os.remove(file_path)

            return render_template('dashboard.html',
                                   result=result,
                                   details=details,
                                   username=session['user'])

        except Exception as e:
            flash(f"Error during analysis: {e}", "error")
    return render_template("dashboard.html", result=result, details=details, username=session["user"])


    #return render_template('dashboard.html', username=session['user'])


@app.route('/signout')
def signout():
    session.pop('user', None)
    flash("You have been signed out.", "info")
    return redirect('/Login')


# === START SERVER ===
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
