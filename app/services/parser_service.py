import re

from app.data.skills import SKILLS


# -------------------------------
# Extract Email
# -------------------------------

def extract_email(text: str):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    return match.group(0) if match else None


# -------------------------------
# Extract Phone Number
# -------------------------------

def extract_phone(text: str):

    pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    return match.group(0) if match else None


# -------------------------------
# Extract Skills
# -------------------------------

def extract_skills(text: str):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text_lower:

            found_skills.append(skill)

    return sorted(list(set(found_skills)))

def extract_name(text: str):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 2 and len(line.split()) <= 4:

            return line

    return None

def extract_experience(text: str):

    pattern = r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return float(match.group(1))

    return 0

def parse_resume(text: str):

    return {

        "candidate_name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "experience_years": extract_experience(text)
    }

