#!/usr/bin/env python3
"""
Profile & Word Cloud Extractor for CV Documents.
Analyzes docs/dossier.md and src/cv-standard.md to dynamically derive:
- target_roles (for job board API search queries)
- technologies, methods, domains & certifications (word cloud)
- scoring_weights (dynamic weights for match scoring)
Generates docs/profile.json.
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple, Any, Set

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "docs"
DOSSIER_FILE = DOCS_DIR / "dossier.md"
PROFILE_FILE = DOCS_DIR / "profile.json"
CV_STANDARD_FILE = BASE_DIR / "src" / "cv-standard.md"

# Universal technical and domain vocabulary taxonomy
KNOWN_TECH = {
    # Languages & Scripting
    "sql", "pl/sql", "plsql", "python", "bash", "shell", "powershell", "java", "c#", "c++",
    "javascript", "typescript", "scala", "go", "golang", "rust", "vba", "php", "ruby", "perl",
    # Databases & Big Data
    "oracle", "postgresql", "postgres", "mysql", "mssql", "sql server", "sqlite",
    "mongodb", "elasticsearch", "kibana", "redis", "cassandra", "snowflake", "bigquery",
    "databricks", "spark", "hadoop", "kafka", "dbt", "airflow",
    # Cloud & Infrastructure
    "azure", "aws", "gcp", "google cloud", "docker", "kubernetes", "k8s", "terraform",
    "ansible", "linux", "unix", "windows server", "git", "github", "gitlab", "ci/cd",
    # Architecture, APIs & Middleware
    "rest", "rest api", "rest apis", "api", "apis", "graphql", "soap", "json", "xml",
    "microservices", "etl", "elt", "dwh", "data warehouse", "data lake", "data mesh",
    "tomcat", "wildfly", "jboss", "weblogic", "iis",
    # Domain & Enterprise Systems
    "syrius", "sap", "salesforce", "servicenow", "jira", "confluence", "sharepoint",
    "iam", "ciam", "access management", "identity management", "active directory",
    "dms", "oms", "ecm", "input management", "output management", "docprostar", "kodak",
    # Data Science & AI
    "data science", "data engineering", "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "bi", "power bi", "tableau"
}

KNOWN_METHODS_DOMAINS = {
    "requirements engineering", "business engineering", "business analysis", "business analyse",
    "anforderungsmanagement", "solution design", "solution engineering", "solution architecture",
    "systemarchitektur", "datenmodellierung", "data modeling", "prozessmanagement", "bpmn", "bpm",
    "use cases", "user stories", "agile", "scrum", "kanban", "safe", "waterfall",
    "testing", "testmanagement", "qualitätsmanagement", "fehleranalyse", "troubleshooting",
    "störungsmanagement", "monitoring", "datenqualität", "governance", "compliance",
    "krankenversicherung", "versicherung", "bank", "banking", "telekommunikation", "retail",
    "migration", "systemmigration", "datenmigration", "bereitstellung", "automatisierung"
}

KNOWN_CERTS_EDU = {
    "ireb", "ipma", "itil", "pmp", "prince2", "scrum master", "product owner",
    "cas", "mas", "das", "bachelor", "master", "diplom", "efz", "berufsmaturität",
    "zhaw", "eth", "uni", "universität", "fachhochschule", "hwz", "sgo"
}

ROLE_TAXONOMY = [
    "Business Engineer", "Requirements Engineer", "IT Business Analyst", "Business Analyst",
    "Solution Designer", "Solution Engineer", "Solution Architect",
    "Data Engineer", "Data Scientist", "Data Analyst", "Analytics Engineer",
    "Product Owner", "Technical Consultant", "IT Consultant",
    "Input Engineer", "Output Management", "Dokumentenmanagement", "ECM Specialist",
    "System Administrator", "Systems Engineer", "Software Engineer", "Software Developer",
    "DevOps Engineer", "Cloud Architect", "Cloud Engineer", "Database Administrator"
]

ROLE_FILTER_KEYWORDS = [
    "engineer", "analyst", "designer", "architect", "developer", "consultant",
    "manager", "specialist", "administrator", "owner", "lead", "leiter", "entwickler",
    "berater", "expert", "management"
]


def extract_text_from_dossier() -> str:
    """Read the full text of docs/dossier.md."""
    if not DOSSIER_FILE.exists():
        return ""
    try:
        return DOSSIER_FILE.read_text(encoding="utf-8")
    except Exception:
        return ""


def extract_text_from_cv() -> str:
    """Read src/cv-standard.md if available."""
    if not CV_STANDARD_FILE.exists():
        return ""
    try:
        return CV_STANDARD_FILE.read_text(encoding="utf-8")
    except Exception:
        return ""


def is_valid_role_name(role: str) -> bool:
    """Filter out non-role sentences or vague phrases."""
    r_lower = role.lower().strip()
    if len(r_lower) < 3 or len(r_lower) > 40:
        return False
    if any(bad in r_lower for bad in ["verschiedene", "lehre", "angestellt", "aufgabengebiet", "tätigkeiten", "zeugnis"]):
        return False
    return any(kw in r_lower for kw in ROLE_FILTER_KEYWORDS)


def find_roles(text: str, cv_text: str) -> List[str]:
    """Identify target roles based on dossier text, CV title, and experience patterns."""
    detected_roles: Counter = Counter()
    combined_text_lower = f"{cv_text}\n{text}".lower()

    # 1. Frontmatter CV title priority
    if cv_text:
        title_match = re.search(r'^title:\s*(.+)$', cv_text, re.MULTILINE | re.IGNORECASE)
        if title_match:
            cv_title = title_match.group(1).strip()
            if is_valid_role_name(cv_title):
                detected_roles[cv_title] += 25

    # 2. Match against role taxonomy
    for role in ROLE_TAXONOMY:
        pattern = r'(?:^|[\s\-_/,\.;:\(\)\[\]])' + re.escape(role.lower()) + r'(?:$|[\s\-_/,\.;:\(\)\[\]])'
        matches = len(re.findall(pattern, combined_text_lower))
        if matches > 0:
            detected_roles[role] += matches * 2

    # 3. Detect roles in experience headers (e.g. \experienceitem{Title}{Company}{Date})
    exp_matches = re.findall(r'\\experienceitem\{([^}]+)\}', cv_text)
    for exp_title in exp_matches:
        clean = exp_title.strip()
        if not is_valid_role_name(clean):
            continue
        matched_known = False
        for role in ROLE_TAXONOMY:
            if role.lower() in clean.lower() or clean.lower() in role.lower():
                detected_roles[role] += 12
                matched_known = True
        if not matched_known:
            detected_roles[clean] += 8

    # 4. Extract roles from certificate phrases: "als [Rolle]", "Funktion als [Rolle]"
    role_phrases = re.findall(
        r'(?:tätig als|angestellt als|funktion als|rolle als)\s+([A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\-\s]{3,35})(?:[,\.\n]|im Bereich|in der)',
        text
    )
    for phrase in role_phrases:
        clean = phrase.strip()
        if not is_valid_role_name(clean):
            continue
        for role in ROLE_TAXONOMY:
            if role.lower() in clean.lower():
                detected_roles[role] += 6

    # Order by frequency/weight
    valid_roles = [role for role, _ in detected_roles.most_common(12) if is_valid_role_name(role)]
    return valid_roles if valid_roles else ["Business Engineer", "IT Business Analyst", "Data Engineer"]


def extract_keywords_with_frequencies(text: str, cv_text: str) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
    """Extract and score technologies, methods, and certifications from text."""
    combined = f"{cv_text}\n{text}".lower()

    tech_counts: Counter = Counter()
    method_counts: Counter = Counter()
    cert_counts: Counter = Counter()

    # Search known tech
    for kw in KNOWN_TECH:
        pattern = r'(?:^|[\s\-_/,\.;:\(\)\[\]])' + re.escape(kw) + r'(?:$|[\s\-_/,\.;:\(\)\[\]])'
        cnt = len(re.findall(pattern, combined))
        if cnt > 0:
            tech_counts[kw] = cnt

    # Search known methods/domains
    for kw in KNOWN_METHODS_DOMAINS:
        pattern = r'(?:^|[\s\-_/,\.;:\(\)\[\]])' + re.escape(kw) + r'(?:$|[\s\-_/,\.;:\(\)\[\]])'
        cnt = len(re.findall(pattern, combined))
        if cnt > 0:
            method_counts[kw] = cnt

    # Search known certs/edu
    for kw in KNOWN_CERTS_EDU:
        pattern = r'(?:^|[\s\-_/,\.;:\(\)\[\]])' + re.escape(kw) + r'(?:$|[\s\-_/,\.;:\(\)\[\]])'
        cnt = len(re.findall(pattern, combined))
        if cnt > 0:
            cert_counts[kw] = cnt

    return dict(tech_counts), dict(method_counts), dict(cert_counts)


def calculate_scoring_weights(tech_counts: Dict[str, int], method_counts: Dict[str, int]) -> Dict[str, int]:
    """Calculate normalized point weights (3-9 points) for each technology/domain skill."""
    weights: Dict[str, int] = {}

    all_items = {**tech_counts, **method_counts}
    if not all_items:
        return {"sql": 7, "python": 6, "oracle": 7, "etl": 6, "requirements engineering": 7}

    max_count = max(all_items.values()) if all_items else 1

    for kw, cnt in all_items.items():
        norm = cnt / max_count
        if norm >= 0.6:
            score = 9 if cnt >= 5 else 8
        elif norm >= 0.3:
            score = 7
        elif norm >= 0.15:
            score = 6
        elif cnt >= 2:
            score = 5
        else:
            score = 4
        weights[kw] = score

    return weights


def calculate_edu_weights(cert_counts: Dict[str, int]) -> Dict[str, int]:
    """Calculate point weights for education and certifications."""
    edu_weights: Dict[str, int] = {}
    base_edu = {
        "cas": 7, "mas": 6, "bachelor": 5, "master": 6, "hochschule": 4, "fachhochschule": 4, "zhaw": 5,
        "studium": 4, "informatik": 5, "computer science": 5, "fh": 3, "uni": 3, "eth": 3,
        "ireb": 7, "ipma": 6, "itil": 5, "scrum": 4, "agil": 3, "product owner": 6
    }
    for kw, default_pts in base_edu.items():
        if kw in cert_counts:
            edu_weights[kw] = min(8, default_pts + (1 if cert_counts[kw] >= 2 else 0))
        else:
            edu_weights[kw] = default_pts
    return edu_weights


def build_profile(output_file: Path = PROFILE_FILE) -> Dict[str, Any]:
    """Extract profile from dossier.md and cv-standard.md and save docs/profile.json."""
    dossier_text = extract_text_from_dossier()
    cv_text = extract_text_from_cv()

    target_roles = find_roles(dossier_text, cv_text)
    tech_counts, method_counts, cert_counts = extract_keywords_with_frequencies(dossier_text, cv_text)
    scoring_weights = calculate_scoring_weights(tech_counts, method_counts)
    edu_weights = calculate_edu_weights(cert_counts)

    # Count docs from dossier headings
    doc_matches = len(re.findall(r'^### 📄', dossier_text, re.MULTILINE))

    profile_data = {
        "last_synced": datetime.now().isoformat(),
        "total_documents": doc_matches,
        "target_roles": target_roles,
        "competencies": {
          "technologies": sorted(list(tech_counts.keys()), key=lambda k: tech_counts[k], reverse=True),
          "methods_domains": sorted(list(method_counts.keys()), key=lambda k: method_counts[k], reverse=True),
          "certifications": sorted(list(cert_counts.keys()), key=lambda k: cert_counts[k], reverse=True)
        },
        "scoring_weights": scoring_weights,
        "edu_weights": edu_weights
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2, ensure_ascii=False)

    return profile_data


def main():
    print("# 🔍 Dynamischer Profil- & Keyword-Extraktor\n")
    profile = build_profile()
    roles = ", ".join(profile.get("target_roles", [])[:5])
    tech_top = ", ".join(profile.get("competencies", {}).get("technologies", [])[:8])
    weights_count = len(profile.get("scoring_weights", {}))
    print(f"✓ Profil erfolgreich generiert: {PROFILE_FILE.relative_to(BASE_DIR)}")
    print(f"• Rollen ({len(profile.get('target_roles', []))}): {roles} ...")
    print(f"• Top-Technologien: {tech_top}")
    print(f"• Dynamische Keyword-Scoring-Gewichte: {weights_count} Begriffe ermittelt.")


if __name__ == "__main__":
    main()
