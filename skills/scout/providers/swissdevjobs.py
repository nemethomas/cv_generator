#!/usr/bin/env python3
"""
SwissDevJobs JSON-Feed provider adapter.
"""

import json
import urllib.request
from typing import List, Optional, Dict, Any

from .base import BaseJobProvider, JobItem

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Accept": "application/json"
}


def fetch_json(url: str) -> Optional[Any]:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as res:
            if res.status == 200:
                return json.loads(res.read().decode("utf-8"))
    except Exception:
        return None
    return None


class SwissDevJobsProvider(BaseJobProvider):
    name: str = "SwissDevJobs"
    FEED_URL: str = "https://swissdevjobs.ch/api/jobsLight"

    def search(self, target_roles: List[str], location: str) -> List[JobItem]:
        source_cfg = self.config.get("sources", {}).get("swissdevjobs", {})
        feed_url = source_cfg.get("feed_url", self.FEED_URL)
        data = fetch_json(feed_url)
        if not data or not isinstance(data, list):
            return []

        allowed_regions = [r.lower() for r in self.config.get("location", {}).get("allowed_regions", ["Zürich"])]
        allowed_regions.extend(["zurich", "zh"])

        items: List[JobItem] = []
        for raw in data:
            if raw.get("isPaused", False):
                continue

            city = raw.get("cityCategory", "") or raw.get("actualCity", "") or ""
            city_lower = city.lower()
            if not any(r in city_lower for r in allowed_regions):
                continue

            title = raw.get("name", "")
            company = raw.get("company", "Unbekannt")
            techs = raw.get("technologies", []) or []
            preview_text = f"{title} | Technologies: {', '.join(techs)}"
            slug = raw.get("jobUrl", "")
            raw_id = raw.get("_id", slug)
            job_url = f"https://swissdevjobs.ch/jobs/{slug}" if slug else "https://swissdevjobs.ch"
            pub_date = (raw.get("activeFrom", "") or "")[:10]

            item = JobItem(
                source=self.name,
                id=f"sdj:{raw_id}",
                title=title,
                company=company,
                place=city or "Zürich",
                date=pub_date,
                url=job_url,
                preview=preview_text,
                skills=techs
            )
            items.append(item)

        return items

    def fetch_full_text(self, job_id: str) -> Optional[Dict[str, Any]]:
        clean_id = job_id.replace("sdj:", "").strip()
        data = fetch_json(self.FEED_URL)
        if not data or not isinstance(data, list):
            return None

        target = next((j for j in data if j.get("_id") == clean_id or j.get("jobUrl") == clean_id), None)
        if not target:
            return None

        title = target.get("name", "Stellenangebot")
        company = target.get("company", "Unternehmen")
        city = target.get("actualCity") or target.get("cityCategory") or "Zürich"
        slug = target.get("jobUrl", "")
        pub_date = (target.get("activeFrom", "") or "")[:10]
        job_url = f"https://swissdevjobs.ch/jobs/{slug}" if slug else "https://swissdevjobs.ch"
        techs = target.get("technologies", []) or []

        description = f"""Technologie-Stack: {', '.join(techs)}
Standort: {city}
Unternehmen: {company}
Inserat-Link: {job_url}
"""
        return {
            "title": title,
            "company": company,
            "place": city,
            "date": pub_date,
            "url": job_url,
            "id": f"sdj:{clean_id}",
            "description": description,
            "skills": techs
        }
