#!/usr/bin/env python3
"""
Job Scout & Match Analyzer for Swiss Job Market (Zürich & Agglomeration).
Searches portals (jobs.ch API) and company career endpoints, applies Black-/Whitelist filters,
and calculates Evidence Match Scores against work certificates (docs/) and profile (src/cv-standard.md).
"""

import sys
import os
import re
import json
import html
import argparse
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = Path(__file__).resolve().parent / "config.json"
JOBS_DIR = BASE_DIR / "jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de-CH,de;q=0.9,en;q=0.8"
}


def load_config():
    """Load configuration from config.json or use sensible defaults."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warnung: Konfiguration konnte nicht geladen werden: {e}", file=sys.stderr)
    return {
        "location": {
            "primary": "Zürich",
            "allowed_regions": ["Zürich", "Altstetten", "Dietikon", "Dübendorf", "Wallisellen"]
        },
        "workload": {"min_percentage": 60, "max_percentage": 100},
        "whitelist_companies": [
            {"name": "Swisscom", "aliases": ["Swisscom", "Swisscom (Schweiz) AG", "localsearch"], "career_url": "https://jobs.swisscom.ch"},
            {"name": "Zürcher Kantonalbank", "aliases": ["ZKB", "Zürcher Kantonalbank AG", "Zürcher Kantonalbank"], "career_url": "https://www.zkb.ch/karriere"},
            {"name": "Google", "aliases": ["Google", "Google Switzerland", "Google Switzerland GmbH", "Google Inc."], "career_url": "https://careers.google.com"},
            {"name": "Zühlke Informatik", "aliases": ["Zühlke", "Zühlke Engineering AG", "Zühlke Group", "Zuehlke"], "career_url": "https://www.zuehlke.com/de/karriere"},
            {"name": "Inventx", "aliases": ["Inventx", "Inventx AG", "Inventix"], "career_url": "https://inventx.ch/karriere"}
        ],
        "blacklist_companies": ["RUAG", "RUAG MRO Holding", "RUAG Defence", "RUAG Space", "RUAG AG"],
        "target_roles": [
            "Business Engineer", "Requirements Engineer", "IT Business Analyst",
            "Solution Designer", "Data Engineer", "Data Scientist", "Product Owner", "Technical Consultant"
        ],
        "core_competencies": [
            "Oracle", "SQL", "PL/SQL", "Python", "SYRIUS", "ETL", "DWH",
            "Data Engineering", "Data Science", "Machine Learning", "Migration",
            "IAM", "Berechtigungen", "APIs", "REST", "Krankenversicherung",
            "Leistungen", "Bestand", "IREB", "IPMA", "ITIL"
        ]
    }


def is_blacklisted(company_name, blacklist):
    """Check if company name matches any blacklisted entry."""
    if not company_name:
        return False
    company_lower = company_name.lower().strip()
    for b in blacklist:
        b_lower = b.lower().strip()
        if b_lower in company_lower or company_lower in b_lower:
            return True
    return False


def is_whitelisted(company_name, whitelist_companies):
    """Check if company name matches any whitelisted company or alias."""
    if not company_name:
        return False, None
    comp_clean = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
    for w in whitelist_companies:
        w_name = w.get("name", "")
        w_clean = re.sub(r'[^a-zA-Z0-9]', '', w_name.lower())
        if w_clean and (w_clean == comp_clean or w_clean in comp_clean):
            return True, w_name
        for alias in w.get("aliases", []):
            a_clean = re.sub(r'[^a-zA-Z0-9]', '', alias.lower())
            if a_clean and (a_clean == comp_clean or a_clean in comp_clean or comp_clean in a_clean):
                return True, w_name
    return False, None


def is_location_allowed(place, allowed_regions):
    """Verify if place is in allowed agglomeration list."""
    if not place:
        return True
    p_lower = place.lower()
    for region in allowed_regions:
        if region.lower() in p_lower:
            return True
    if "zürich" in p_lower or "zurich" in p_lower or "zh" in p_lower:
        return True
    return False


def fetch_json(url, params=None):
    """Fetch JSON from a URL with parameters."""
    if params:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
    else:
        full_url = url
    try:
        req = urllib.request.Request(full_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return None
    return None


def fetch_job_detail(job_id):
    """Fetch complete detail of a job from jobs.ch API."""
    url = f"https://www.jobs.ch/api/v1/public/search/job/{job_id}"
    return fetch_json(url)


def clean_html(raw_html):
    """Remove HTML tags and entities."""
    if not raw_html:
        return ""
    # Unescape HTML entities first (&uuml; -> ü, etc.)
    unescaped = html.unescape(raw_html)
    # Add newlines for block elements
    formatted = re.sub(r'<(p|br|div|li|h[1-6])[^>]*>', '\n', unescaped, flags=re.IGNORECASE)
    # Strip remaining tags
    clean = re.sub(r'<[^<]+?>', ' ', formatted)
    # Clean whitespace
    lines = [line.strip() for line in clean.split('\n') if line.strip()]
    return '\n\n'.join(lines)


def calculate_match_score(title, description, company_name, config):
    """
    Calculate an evidence match score (0-100%) against CV profile and certificates.
    Profile strengths:
      - Oracle, SQL, PL/SQL, ETL, DWH, Python, Data Engineering, Data Science, Machine Learning
      - Adcubum SYRIUS, Migration, Versicherung (Leistungen, Bestand), Inputmanagement
      - Requirements Engineering, BPMN, IREB, CAS BA, CAS PM, ITIL, IPMA
      - IAM, Berechtigungen, Access Management, Unix/Linux, REST APIs
    """
    text = f"{title} {description} {company_name}".lower()
    score = 45  # Base score for matching geographic and role filters

    # Tech & Domain skills matching (up to +40)
    tech_keywords = {
        "sql": 7, "oracle": 7, "pl/sql": 6, "python": 6,
        "data engineering": 8, "data scientist": 8, "data science": 8, "machine learning": 6,
        "etl": 6, "dwh": 6, "data warehouse": 6, "elasticsearch": 4, "kibana": 4,
        "syrius": 9, "adcubum": 9, "migration": 6, "versicherung": 5, "krankenversicherung": 5,
        "input engineer": 8, "dokumentenmanagement": 8, "inputmanagement": 8, "input management": 8,
        "dms": 6, "oms": 6, "ecm": 6, "archiv": 5, "kodak": 5, "docprostar": 5,
        "business analyst": 8, "business analysis": 8, "business analyse": 8,
        "business engineer": 8, "business engineering": 8,
        "requirements engineer": 7, "requirements engineering": 7, "anforderungsmanagement": 6,
        "solution designer": 7, "solution design": 7, "product owner": 6,
        "use cases": 4, "user stories": 4, "bpmn": 4,
        "access management": 7, "identity": 6, "ciam": 6, "iam": 6, "berechtigung": 5, "rollenmodell": 5,
        "api": 4, "rest": 4, "linux": 3, "unix": 3, "devops": 4
    }

    matched_tech = []
    tech_points = 0
    for kw, pts in tech_keywords.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            tech_points += pts
            matched_tech.append(kw)
    score += min(40, tech_points)

    # Education & Certification matching (up to +10)
    edu_keywords = {
        "cas": 5, "mas": 4, "bachelor": 4, "master": 4, "hochschule": 3, "fachhochschule": 3, "zhaw": 4,
        "ireb": 5, "ipma": 4, "itil": 4, "scrum": 3, "agil": 3
    }
    for kw, pts in edu_keywords.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            score += pts
            matched_tech.append(kw)
            break

    # Whitelist Bonus (+15)
    is_white, white_name = is_whitelisted(company_name, config.get("whitelist_companies", []))
    if is_white:
        score += 15

    final_score = min(98, max(45, score))
    return final_score, list(set(matched_tech)), is_white, white_name


def search_jobs(query=None, whitelist_only=False, max_results=12):
    """Search jobs.ch for positions matching criteria."""
    config = load_config()
    allowed_regions = config.get("location", {}).get("allowed_regions", ["Zürich"])
    blacklist = config.get("blacklist_companies", [])
    whitelist = config.get("whitelist_companies", [])
    target_roles = config.get("target_roles", ["Business Engineer"])
    primary_loc = config.get("location", {}).get("primary", "Zürich")

    queries_to_run = []
    if query:
        # User supplied explicit query
        queries_to_run = [f"{query} {primary_loc}"]
    elif whitelist_only:
        # Search specifically for whitelist companies
        for w in whitelist:
            queries_to_run.append(f"{w['name']} {primary_loc}")
            for role in ["Engineer", "Data", "Business Analyst"]:
                queries_to_run.append(f"{w['name']} {role}")
    else:
        # Standard search for target roles
        for r in target_roles:
            queries_to_run.append(f"{r} {primary_loc}")
        # Add whitelist companies to search batch
        for w in whitelist:
            queries_to_run.append(f"{w['name']} {primary_loc}")

    all_jobs = []
    seen_ids = set()
    search_url = "https://www.jobs.ch/api/v1/public/search"

    for q in queries_to_run:
        # For whitelist queries or target queries, fetch up to 4 pages (80 jobs per company/term)
        is_company_query = any(w["name"].lower() in q.lower() for w in whitelist)
        max_pages = 4 if (whitelist_only or is_company_query) else 2

        for page in range(1, max_pages + 1):
            params = {
                "query": q,
                "rows": 20,
                "page": page
            }
            res = fetch_json(search_url, params=params)
            if not res or "documents" not in res:
                break

            docs = res.get("documents", [])
            if not docs:
                break

            for doc in docs:
                job_id = doc.get("job_id")
                if not job_id or job_id in seen_ids:
                    continue
                seen_ids.add(job_id)

                company = doc.get("company_name", "Unbekannt")
                title = doc.get("title", "")
                place = doc.get("place", "")

                # 1. Blacklist check
                if is_blacklisted(company, blacklist):
                    continue

                # 2. Location check
                if not is_location_allowed(place, allowed_regions):
                    continue

                # 3. Whitelist-only filter check
                is_white, white_name = is_whitelisted(company, whitelist)
                if whitelist_only and not is_white:
                    continue

                # Extract basic preview description
                preview = doc.get("preview", "")
                publication_date = doc.get("publication_date", "")[:10]
                job_url = f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"

                score, matched_kws, is_white_match, matched_wh_name = calculate_match_score(
                    title, preview, company, config
                )

                all_jobs.append({
                    "id": job_id,
                    "title": title,
                    "company": company,
                    "place": place,
                    "date": publication_date,
                    "url": job_url,
                    "score": score,
                    "is_whitelist": is_white_match,
                    "whitelist_name": matched_wh_name,
                    "keywords": matched_kws,
                    "preview": preview
                })

            if len(docs) < 20:
                # No more pages available
                break

    # Deduplicate by (company, title)
    unique_jobs = []
    seen_comp_title = set()
    for j in all_jobs:
        norm_title = re.sub(r'[\(\[\{].*?[\)\]\}]', '', j["title"]).strip().lower()
        key = (j["company"].lower().strip(), norm_title)
        if key not in seen_comp_title:
            seen_comp_title.add(key)
            unique_jobs.append(j)

    # Sort by score descending (whitelist jobs receive a +15 score bonus and are marked with ⭐)
    unique_jobs.sort(key=lambda x: x["score"], reverse=True)
    return unique_jobs[:max_results]


def export_job_to_markdown(job_id_or_data, target_file=None):
    """Download full job detail and export to markdown in jobs/ directory."""
    JOBS_DIR.mkdir(parents=True, exist_ok=True)

    if isinstance(job_id_or_data, dict):
        job_id = job_id_or_data.get("id")
    else:
        job_id = str(job_id_or_data).strip()

    detail = fetch_job_detail(job_id)
    if not detail:
        print(f"Fehler: Detaildaten für Job-ID '{job_id}' konnten nicht geladen werden.", file=sys.stderr)
        return None

    title = detail.get("title", "Stellenangebot")
    company = detail.get("company_name", "Unternehmen")
    place = detail.get("place", "Zürich")
    pub_date = detail.get("publication_date", "")[:10]
    job_url = f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"

    # Extract template description
    template = detail.get("template", "")
    description_text = clean_html(template) if template else detail.get("preview", "")

    skills_list = detail.get("skills", [])
    skills_formatted = ", ".join(skills_list) if skills_list else "Nicht separat aufgeführt"

    # Create slug for filename
    comp_slug = re.sub(r'[^a-zA-Z0-9]', '', company.lower())[:15]
    title_slug = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())[:30]
    filename = target_file or f"{comp_slug}-{title_slug}.md"
    file_path = JOBS_DIR / filename

    content = f"""# Stellenbeschreibung: {title}

**Unternehmen:** {company}  
**Standort:** {place}  
**Datum:** {pub_date}  
**Quelle:** [{job_url}]({job_url})  
**ID:** `{job_id}`  

---

## Anforderungsprofil & Aufgaben

{description_text}

---

## Extrahierte Kernkompetenzen (ATS)
{skills_formatted}
"""
    file_path.write_text(content, encoding="utf-8")
    return file_path


def analyze_single_url(url):
    """Analyze a single job posting URL."""
    match = re.search(r'detail/([a-f0-9\-]+)', url)
    if match:
        job_id = match.group(1)
        detail = fetch_job_detail(job_id)
        if detail:
            config = load_config()
            title = detail.get("title", "")
            company = detail.get("company_name", "")
            place = detail.get("place", "")
            desc = clean_html(detail.get("template", detail.get("preview", "")))
            score, matched_kws, is_white, white_name = calculate_match_score(title, desc, company, config)

            badge = "🟢" if score >= 80 else ("🟡" if score >= 65 else "🔴")
            print(f"# 🎯 Job-Scout Einzelanalyse\n")
            print(f"**Stelle:** {title}")
            print(f"**Unternehmen:** {company} {'⭐ (Whitelist: ' + white_name + ')' if is_white else ''}")
            print(f"**Standort:** {place}")
            print(f"**Match-Score:** {badge} **{score} %**\n")
            print(f"**Gefundene Profil-Keywords:** {', '.join(matched_kws[:10])}\n")
            print(f"**Direktlink:** {url}\n")

            saved_path = export_job_to_markdown(job_id)
            if saved_path:
                print(f"✓ Als Stellenprofil gespeichert unter: `{saved_path.relative_to(BASE_DIR)}`")
                print(f"➡️ Du kannst nun `/fit {saved_path.stem}` oder `/make {saved_path.stem}` ausführen.")
            return
    print(f"Analysiere externe URL: {url}...")


def main():
    parser = argparse.ArgumentParser(description="Job Scout & Evidence Matcher")
    parser.add_argument("query", nargs="?", default=None, help="Suchbegriff, Job-Rolle, Firma oder URL")
    parser.add_argument("--whitelist", action="store_true", help="Nur Whitelist-Unternehmen (Swisscom, ZKB, Google, Zühlke, Inventx) durchsuchen")
    parser.add_argument("--save", type=str, default=None, help="Job-ID oder Index zum Speichern in jobs/")
    parser.add_argument("--limit", type=int, default=10, help="Anzahl der Treffer (Standard: 10)")
    args = parser.parse_args()

    if args.query and (args.query.startswith("http://") or args.query.startswith("https://")):
        analyze_single_url(args.query)
        return

    if args.save:
        saved_file = export_job_to_markdown(args.save)
        if saved_file:
            print(f"✓ Stellenbeschreibung erfolgreich gespeichert: {saved_file}")
        return

    print(f"# 🧭 Job Scout: Stellenangebote im Grossraum Zürich\n")
    if args.whitelist:
        print("🔍 **Modus:** Whitelist-Fokus (*Swisscom, ZKB, Google, Zühlke Informatik, Inventx*)")
    elif args.query:
        print(f"🔍 **Suchbegriff:** `{args.query}` (Zürich & Agglo, Pensum >= 60%)")
    else:
        print("🔍 **Suchbereich:** Zürich, Altstetten, Dietikon, Dübendorf, Wallisellen (Pensum >= 60%)")
        print("🎯 **Fokus:** Business Engineering, Data Engineering, Data Science, Requirements Engineering")

    print("🛡️ **Ausschluss:** RUAG (Blacklist aktiv)\n")

    jobs = search_jobs(query=args.query, whitelist_only=args.whitelist, max_results=args.limit)

    if not jobs:
        print("ℹ️ Keine neuen offenen Stellen für die angegebenen Kriterien gefunden.")
        return

    print("| # | Score | Stelle / Rolle | Unternehmen | Ort | Datum | Aktion |")
    print("| :-: | :---: | :--- | :--- | :--- | :---: | :--- |")
    for idx, j in enumerate(jobs, 1):
        badge = "🟢" if j["score"] >= 80 else ("🟡" if j["score"] >= 65 else "🔴")
        wh_star = " ⭐" if j["is_whitelist"] else ""
        comp_str = f"{j['company']}{wh_star}"
        print(f"| {idx} | {badge} **{j['score']}%** | [{j['title']}]({j['url']}) | {comp_str} | {j['place']} | {j['date']} | `python3 skills/scout/search_jobs.py --save {j['id']}` |")

    print("\n---\n")
    print("💡 **Legende:** ⭐ = Whitelist-Unternehmen | 🟢 = Hoher Match (>=80%) | 🟡 = Moderater Match (65-79%)")
    print("- **Stelle importieren:** Führe den Befehl in der Spalte `Aktion` aus, um das Inserat nach `jobs/` zu speichern.")
    print("- **Passgenauigkeit prüfen:** `/fit <firma>` berechnet den exakten Match gegen deinen Lebenslauf.")
    print("- **Lebenslauf generieren:** `make <firma>` erstellt dein massgeschneidertes PDF.")


if __name__ == "__main__":
    main()
