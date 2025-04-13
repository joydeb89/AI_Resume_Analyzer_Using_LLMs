import re

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d{1,3})?\s*[\(]?\d{3}[\)]?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group() if match else None

def extract_linkedin(text):
    match = re.search(r'(https?:\/\/)?(www\.)?linkedin\.com\/[a-zA-Z0-9\-_/]+', text)
    return match.group() if match else None

def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines[:5]:  # usually name is at the top
        line = line.strip()
        if len(line.split()) in [2, 3] and line[0].isupper():
            return line
    return None

def extract_skills(text, keywords):
    skills_found = []
    text_lower = text.lower()
    for skill in keywords:
        if skill.lower() in text_lower:
            skills_found.append(skill)
    return list(set(skills_found))

def extract_college(text):
    college_keywords = ["university", "institute", "college", "technology"]
    return [line.strip() for line in text.splitlines() if any(kw in line.lower() for kw in college_keywords)]


def extract_projects_details(text: str) -> list:
    """
    Extracts structured project details from resume text.
    Combines all bullet points into a single description for each project.
    """
    lines = text.splitlines()
    projects = []
    current_project = None
    in_project_section = False

    for line in lines:
        # Detect "PROJECTS" section
        if not in_project_section:
            if "PROJECTS" in line.upper():
                in_project_section = True
            continue

        # Stop if new section starts
        if line.strip() and line.strip().isupper() and not line.startswith(("•", "-", "*", "◦")):
            break

        # New project
        if line.lstrip().startswith(("•", "-", "*")):
            if current_project:
                # ✅ Combine all bullets into a single paragraph
                description = " ".join(current_project["bullets"])
                current_project["bullets"] = [description.strip()]
                projects.append(current_project)
            current_project = {"title": "", "duration": "", "tools": "", "bullets": []}
            clean_line = line.lstrip("•-* ").strip()
            match = re.match(r"(.+?)(?::\s*(.+))?$", clean_line)
            if match:
                current_project["title"] = match.group(1).strip()
                if match.group(2):
                    current_project["duration"] = match.group(2).strip()
            else:
                current_project["title"] = clean_line
            continue

        # Tools
        if "tools:" in line.lower():
            tools = re.split(r"tools:", line, flags=re.IGNORECASE)[-1].strip()
            tools = re.sub(r"[\[\]]", "", tools)
            current_project["tools"] = tools
            continue

        # Description lines
        if current_project:
            if line.lstrip().startswith(("◦", "-", "*", "•")):
                current_project["bullets"].append(line.lstrip("•-*◦ ").strip())
            elif len(line.split()) > 2:
                current_project["bullets"].append(line.strip())

    # Add final project
    if current_project:
        description = " ".join(current_project["bullets"])
        current_project["bullets"] = [description.strip()]
        projects.append(current_project)

    return projects



def extract_certifications_details(text: str) -> list:
    """
    Extracts structured certification details from resume text.
    Looks for lines under a CERTIFICATIONS section or lines with 'certification' or 'certificate'.
    """
    lines = text.splitlines()
    certifications = []
    in_cert_section = False

    for line in lines:
        if not in_cert_section:
            if "CERTIFICATIONS" in line.upper() or "CERTIFICATION" in line.upper():
                in_cert_section = True
            continue

        # Stop at next all-uppercase section
        if line.strip() and line.strip().isupper() and not line.startswith(("-", "*", "•", "◦")):
            break

        # If line contains certification or certificate
        if re.search(r'certificat(e|ion)', line, re.IGNORECASE):
            certifications.append(line.strip())

        # Bullet points under CERTIFICATIONS
        if line.lstrip().startswith(("•", "-", "◦", "*")):
            certifications.append(line.lstrip("•-◦* ").strip())

    return certifications

def extract_internships_details(text: str) -> list:
    """
    Extracts structured internship details from resume text.
    Combines all bullet points into a single description per internship.
    """
    lines = text.splitlines()
    internships = []
    current = {}
    buffer = []
    in_section = False
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect internship section start
        if not in_section and re.match(r'^INTERNSHIP(S)?( EXPERIENCE)?$', line.upper()):
            in_section = True
            i += 1
            continue

        # Stop if a new unrelated section starts (like EDUCATION, PROJECTS, etc.)
        if in_section and line and line.isupper() and "INTERNSHIP" not in line:
            break

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Assume company name
        if in_section and not current.get("company"):
            current["company"] = line.strip()
            i += 1
            continue

        # Assume internship role/title
        if in_section and not current.get("title"):
            title_line = line.strip()
            current["title"] = title_line if "intern" in title_line.lower() else "Intern"
            i += 1
            continue

        # Capture description lines (bullets or full sentences)
        if in_section:
            if line.startswith(("•", "-", "*", "◦")):
                buffer.append(line.lstrip("•-*◦ ").strip())
            elif len(line.split()) > 2:
                buffer.append(line.strip())

        i += 1

    # Add the final internship
    if current:
        description = " ".join(buffer)
        current["bullets"] = [description.strip()]
        internships.append(current)

    return internships





def extract_experience(text):
    experiences = []
    lines = text.split("\n")
    for line in lines:
        if "experience" in line.lower() or "internship" in line.lower():
            experiences.append(line.strip())
    return experiences

def extract_resume_details(text, skill_keywords=None):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "experience": extract_experience(text),
        "college": extract_college(text),
        "projects": extract_projects_details(text),
        "certifications": extract_certifications_details(text),
        "internships": extract_internships_details(text),
        "skills": skill_keywords or []
    }
