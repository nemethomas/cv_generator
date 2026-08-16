#!/usr/bin/env python3
"""
Job Scout & Match Analyzer for Swiss Job Market (Zürich & Agglomeration).
Multi-Source Architecture: jobs.ch, LinkedIn/Indeed/Glassdoor (JobSpy), SwissDevJobs.
Calculates Evidence Match Scores dynamically based on docs/profile.json (extracted from docs/dossier.md).
"""

import sys
import os
import re
import json
import html
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

# Ensure scout directory is in sys.path for provider imports
SCOUT_DIR = Path(__file__).resolve().parent
if str(SCOUT_DIR) not in sys.path:
    sys.path.insert(0, str(SCOUT_DIR))

from providers import get_enabled_providers, fetch_full_job_data
from providers.base import JobItem

BASE_DIR = Path(__file__).resolve().parents[2]
DOCS_DIR = BASE_DIR / "docs"
CONFIG_FILE = SCOUT_DIR / "config.json"
JOBS_DIR = BASE_DIR / "jobs"
PROFILE_FILE = DOCS_DIR / "profile.json"
PROFILE_EXAMPLE_FILE = DOCS_DIR / "profile.example.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json or use sensible defaults."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warnung: Konfiguration konnte nicht geladen werden: {e}", file=sys.stderr)
    return {
        "sources": {
            "jobsch": {"enabled": True, "max_pages": 4},
            "jobspy": {"enabled": True, "sites": ["linkedin", "indeed"], "results_wanted": 15},
            "swissdevjobs": {"enabled": True}
        },
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
            {"name": "Inventx", "aliases": ["Inventx", "Inventx AG", "Inventix"], "career_url": "https://inventx.ch/karriere"},
            {"name": "ELCA", "aliases": ["Elca informatique SA", "ELCA AG", "ELCA Group", "ELCA Cloud Services SA", "ELCA Security SA", "ELCA"], "career_url": "https://www.elca.ch/de/karriere"}
        ],
        "blacklist_companies": ["RUAG", "RUAG MRO Holding", "RUAG Defence", "RUAG Space", "RUAG AG"]
    }


def load_profile() -> Dict[str, Any]:
    """Load dynamic candidate profile from docs/profile.json (fallback: profile.example.json)."""
    if PROFILE_FILE.exists():
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warnung: Profil {PROFILE_FILE} konnte nicht gelesen werden: {e}", file=sys.stderr)

    if PROFILE_EXAMPLE_FILE.exists():
        try:
            with open(PROFILE_EXAMPLE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "target_roles": ["Business Engineer", "IT Business Analyst", "Data Engineer"],
        "scoring_weights": {
            "sql": 8, "python": 7, "oracle": 7, "etl": 6, "requirements engineering": 8,
            "data engineering": 8, "syrius": 9, "agile": 6
        },
        "edu_weights": {
            "cas": 7, "master": 6, "bachelor": 5, "ireb": 7, "ipma": 6, "itil": 5
        }
    }


def is_blacklisted(company_name: str, blacklist: List[str]) -> bool:
    """Check if company name matches any blacklisted entry."""
    if not company_name:
        return False
    company_lower = company_name.lower().strip()
    for b in blacklist:
        b_lower = b.lower().strip()
        if b_lower in company_lower or company_lower in b_lower:
            return True
    return False


def is_whitelisted(company_name: str, whitelist_companies: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
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


def is_location_allowed(place: str, allowed_regions: List[str]) -> bool:
    """Verify if place is in allowed agglomeration list."""
    if not place:
        return True
    p_lower = place.lower()
    for region in allowed_regions:
        if region.lower() in p_lower:
            return True
    if "zürich" in p_lower or "zurich" in p_lower or "zh" in p_lower or "switzerland" in p_lower:
        return True
    return False


def calculate_match_score(
    title: str,
    description: str,
    company_name: str,
    config: Dict[str, Any],
    profile: Dict[str, Any]
) -> Tuple[int, List[str], bool, Optional[str]]:
    """
    Calculate dynamic evidence match score (0-100%) against candidate profile (docs/profile.json).
    Weights:
      - Base / Regional & Target Role Fit: 40%
      - Tech- & Domain-Stack (dynamic weights): up to 40%
      - Education & Certifications (dynamic weights): up to 20%
    """
    text = f"{title} {description} {company_name}".lower()
    score = 40  # Base score for role and regional relevance

    scoring_weights = profile.get("scoring_weights", {})
    edu_weights = profile.get("edu_weights", {})

    # Tech & Domain skills matching (up to +40)
    matched_tech = []
    tech_points = 0
    for kw, pts in scoring_weights.items():
        pattern = r'(?:^|[\s\-_/,\.;:\(\)\[\]])' + re.escape(kw.lower()) + r'(?:$|[\s\-_/,\.;:\(\)\[\]])'
        if re.search(pattern, text):
            tech_points += pts
            matched_tech.append(kw)
    score += min(40, tech_points)

    # Education & Certification matching (up to +20)
    edu_points = 0
    for kw, pts in edu_weights.items():
        pattern = r'(?:^|[\s\-_/,\.;:\(\)\[\]])' + re.escape(kw.lower()) + r'(?:$|[\s\-_/,\.;:\(\)\[\]])'
        if re.search(pattern, text):
            edu_points += pts
            matched_tech.append(kw)
    score += min(20, edu_points)

    is_white, white_name = is_whitelisted(company_name, config.get("whitelist_companies", []))
    final_score = min(100, max(40, score))
    return final_score, list(set(matched_tech)), is_white, white_name


def generate_dedup_key(company: str, title: str) -> Tuple[str, str]:
    """Generate normalized tuple key for cross-portal deduplication."""
    clean_company = re.sub(r'[^a-z0-9]', '', company.lower().strip())
    # Strip common suffixes/prefixes (pensum, gender markers, level)
    norm_title = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title.lower())
    norm_title = re.sub(r'\b(m/w/d|80-100%|100%|80%|senior|junior|lead)\b', '', norm_title)
    clean_title = re.sub(r'[^a-z0-9]', '', norm_title.strip())
    return clean_company, clean_title


def search_jobs(query: Optional[str] = None, whitelist_only: bool = False, max_results: int = 15) -> List[JobItem]:
    """
    Search all enabled providers (jobs.ch, JobSpy, SwissDevJobs),
    apply filters, deduplicate cross-portal listings, and calculate Evidence Match Scores.
    """
    config = load_config()
    profile = load_profile()

    allowed_regions = config.get("location", {}).get("allowed_regions", ["Zürich"])
    blacklist = config.get("blacklist_companies", [])
    whitelist = config.get("whitelist_companies", [])
    primary_loc = config.get("location", {}).get("primary", "Zürich")

    if query:
        target_roles = [query]
    else:
        profile_roles = profile.get("target_roles", [])
        target_roles = profile_roles if profile_roles else ["Business Engineer", "IT Business Analyst", "Data Engineer"]

    providers = get_enabled_providers(config)

    raw_items: List[JobItem] = []
    for provider in providers:
        try:
            items = provider.search(target_roles=target_roles, location=primary_loc)
            raw_items.extend(items)
        except Exception as e:
            print(f"Fehler bei Provider {provider.name}: {e}", file=sys.stderr)

    # Process, filter, score and deduplicate
    dedup_dict: Dict[Tuple[str, str], JobItem] = {}

    for item in raw_items:
        # 1. Blacklist check
        if is_blacklisted(item.company, blacklist):
            continue

        # 2. Location check
        if not is_location_allowed(item.place, allowed_regions):
            continue

        # 3. Whitelist-only filter check
        is_white, white_name = is_whitelisted(item.company, whitelist)
        if whitelist_only and not is_white:
            continue

        item.is_whitelist = is_white
        item.whitelist_name = white_name

        # Calculate score dynamically
        desc_to_score = item.description_full or item.preview or ""
        score, matched_kws, _, _ = calculate_match_score(
            item.title, desc_to_score, item.company, config, profile
        )
        item.match_score = score
        item.matched_keywords = matched_kws

        # Cross-portal deduplication
        dedup_key = generate_dedup_key(item.company, item.title)
        if dedup_key in dedup_dict:
            existing = dedup_dict[dedup_key]
            if item.source not in existing.source:
                existing.source = f"{existing.source}, {item.source}"
            if item.match_score > existing.match_score:
                existing.match_score = item.match_score
            if item.description_full and not existing.description_full:
                existing.description_full = item.description_full
        else:
            dedup_dict[dedup_key] = item

    results = list(dedup_dict.values())
    results.sort(key=lambda x: x.match_score, reverse=True)
    return results[:max_results]


def export_job_to_markdown(job_id_or_data: Any, target_file: Optional[str] = None) -> Optional[Path]:
    """Download full job detail and export to markdown in jobs/ directory."""
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()

    if isinstance(job_id_or_data, dict):
        job_id = job_id_or_data.get("id")
    else:
        job_id = str(job_id_or_data).strip()

    detail = fetch_full_job_data(job_id, config)
    if not detail:
        print(f"Fehler: Detaildaten für Job-ID '{job_id}' konnten nicht geladen werden.", file=sys.stderr)
        return None

    title = detail.get("title", "Stellenangebot")
    company = detail.get("company_name", detail.get("company", "Unternehmen"))
    place = detail.get("place", "Zürich")
    pub_date = detail.get("publication_date", detail.get("date", ""))[:10]
    job_url = detail.get("url", "")
    description_text = detail.get("description", "")
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


def main():
    parser = argparse.ArgumentParser(description="Job Scout & Evidence Matcher (Multi-Source)")
    parser.add_argument("query", nargs="?", default=None, help="Suchbegriff, Job-Rolle, Firma oder URL")
    parser.add_argument("--whitelist", action="store_true", help="Nur Whitelist-Unternehmen durchsuchen")
    parser.add_argument("--save", type=str, default=None, help="Job-ID zum Speichern in jobs/")
    parser.add_argument("--limit", type=int, default=12, help="Anzahl der Treffer (Standard: 12)")
    args = parser.parse_args()

    if args.save:
        saved_file = export_job_to_markdown(args.save)
        if saved_file:
            print(f"✓ Stellenbeschreibung erfolgreich gespeichert: {saved_file}")
            print(f"➡️ Du kannst nun `/fit {saved_file.stem}` oder `make {saved_file.stem}` ausführen.")
        return

    config = load_config()
    profile = load_profile()
    sources_cfg = config.get("sources", {})
    active_sources = [k for k, v in sources_cfg.items() if v.get("enabled", True)]

    target_roles = profile.get("target_roles", [])
    roles_preview = ", ".join(target_roles[:4]) if target_roles else "Allgemein"

    print(f"# 🧭 Job Scout: Multi-Source Stellenangebote (Grossraum Zürich)\n")
    print(f"📡 **Aktive Quellen:** {', '.join(active_sources).upper()}")
    if args.whitelist:
        print("🔍 **Modus:** Whitelist-Fokus (*Swisscom, ZKB, Google, Zühlke, Inventx, ELCA, Migros*)")
    elif args.query:
        print(f"🔍 **Suchbegriff:** `{args.query}` (Zürich & Agglo, Pensum >= 60%)")
    else:
        print(f"🔍 **Suchbereich:** Zürich & Agglomeration (Pensum >= 60%)")
        print(f"🎯 **Dynamische Profil-Rollen ({len(target_roles)}):** {roles_preview}")

    print("🛡️ **Ausschluss:** RUAG (Blacklist aktiv)\n")

    jobs = search_jobs(query=args.query, whitelist_only=args.whitelist, max_results=args.limit)

    if not jobs:
        print("ℹ️ Keine neuen offenen Stellen für die angegebenen Kriterien gefunden.")
        return

    print("| # | Score | Stelle / Rolle | Unternehmen | Ort | Quelle | Aktion |")
    print("| :-: | :---: | :--- | :--- | :--- | :---: | :--- |")
    for idx, j in enumerate(jobs, 1):
        badge = "🟢" if j.match_score >= 80 else ("🟡" if j.match_score >= 65 else "🔴")
        print(f"| {idx} | {badge} **{j.match_score}%** | [{j.title}]({j.url}) | {j.company} | {j.place} | `{j.source}` | `python3 skills/scout/search_jobs.py --save \"{j.id}\"` |")

    print("\n---\n")
    print("💡 **Legende:** 🟢 = Hoher Match (>=80%) | 🟡 = Moderater Match (65-79%) | 🔴 = Niedriger Match (<65%)")
    print("- **Stelle importieren:** Führe den Befehl in der Spalte `Aktion` aus, um das Inserat nach `jobs/` zu speichern.")
    print("- **Passgenauigkeit prüfen:** `/fit <firma>` berechnet den exakten Match gegen deinen Lebenslauf.")
    print("- **Lebenslauf generieren:** `make <firma>` erstellt dein massgeschneidertes PDF.")


if __name__ == "__main__":
    main()
