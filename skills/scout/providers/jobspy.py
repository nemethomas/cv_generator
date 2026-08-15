#!/usr/bin/env python3
"""
JobSpy provider adapter (LinkedIn, Indeed, Glassdoor, Google Jobs).
"""

import sys
import datetime
from typing import List, Optional, Dict, Any

from .base import BaseJobProvider, JobItem

import os
import json
from pathlib import Path

CACHE_FILE = Path(__file__).resolve().parents[1] / ".cache_jobs.json"


def _load_cache() -> Dict[str, Dict[str, Any]]:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_cache(cache: Dict[str, Dict[str, Any]]) -> None:
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class JobSpyProvider(BaseJobProvider):
    name: str = "JobSpy"

    def search(self, target_roles: List[str], location: str) -> List[JobItem]:
        try:
            from jobspy import scrape_jobs
        except ImportError:
            print("Hinweis: python-jobspy ist nicht installiert. Überspringe JobSpy-Quellen.", file=sys.stderr)
            return []

        cache = _load_cache()
        source_cfg = self.config.get("sources", {}).get("jobspy", {})
        sites = source_cfg.get("sites", ["linkedin", "indeed"])
        results_wanted = source_cfg.get("results_wanted", 15)

        # Standard search query for JobSpy
        search_loc = f"{location}, Switzerland"
        items: List[JobItem] = []
        seen_urls = set()

        # Query primary target roles
        roles_to_query = target_roles[:5] if len(target_roles) > 5 else target_roles

        for role in roles_to_query:
            try:
                df = scrape_jobs(
                    site_name=sites,
                    search_term=role,
                    location=search_loc,
                    results_wanted=results_wanted,
                    country_indeed="Switzerland"
                )
                if df is None or df.empty:
                    continue

                for _, row in df.iterrows():
                    raw_url = str(row.get("job_url", "") or "")
                    if not raw_url or raw_url in seen_urls:
                        continue
                    seen_urls.add(raw_url)

                    site_name = str(row.get("site", "jobspy") or "jobspy")
                    raw_id = str(row.get("id", "") or "")
                    if not raw_id:
                        raw_id = raw_url.split("/")[-1].split("?")[0]

                    unique_id = f"{site_name}:{raw_id}"
                    title = str(row.get("title", "Stellenangebot") or "")
                    company = str(row.get("company", "Unternehmen") or "")
                    place = str(row.get("location", location) or location)

                    date_val = row.get("date_posted")
                    if isinstance(date_val, (datetime.date, datetime.datetime)):
                        pub_date = date_val.strftime("%Y-%m-%d")
                    else:
                        pub_date = str(date_val or "")[:10]

                    description = str(row.get("description", "") or "")
                    preview = description[:300].strip() if description else title
                    skills_val = row.get("skills")
                    skills_list = [s.strip() for s in str(skills_val).split(",") if s.strip()] if skills_val else []

                    # Store in persistent cache for full export
                    cache[unique_id] = {
                        "title": title,
                        "company": company,
                        "place": place,
                        "date": pub_date,
                        "url": raw_url,
                        "id": unique_id,
                        "description": description,
                        "skills": skills_list
                    }

                    item = JobItem(
                        source=site_name.capitalize(),
                        id=unique_id,
                        title=title,
                        company=company,
                        place=place,
                        date=pub_date,
                        url=raw_url,
                        preview=preview,
                        description_full=description,
                        skills=skills_list
                    )
                    items.append(item)
            except Exception as e:
                print(f"Warnung bei JobSpy-Abfrage ({role}): {e}", file=sys.stderr)
                continue

        _save_cache(cache)
        return items

    def fetch_full_text(self, job_id: str) -> Optional[Dict[str, Any]]:
        cache = _load_cache()
        return cache.get(job_id)
