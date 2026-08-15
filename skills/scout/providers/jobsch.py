#!/usr/bin/env python3
"""
jobs.ch REST-API provider adapter.
"""

import re
import html
import json
import urllib.request
import urllib.parse
from typing import List, Optional, Dict, Any

from .base import BaseJobProvider, JobItem

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de-CH,de;q=0.9,en;q=0.8"
}


def clean_html(raw_html: str) -> str:
    """Remove HTML tags and entities."""
    if not raw_html:
        return ""
    unescaped = html.unescape(raw_html)
    formatted = re.sub(r'<(p|br|div|li|h[1-6])[^>]*>', '\n', unescaped, flags=re.IGNORECASE)
    clean = re.sub(r'<[^<]+?>', ' ', formatted)
    lines = [line.strip() for line in clean.split('\n') if line.strip()]
    return '\n\n'.join(lines)


def fetch_json(url: str, params: Optional[dict] = None) -> Optional[dict]:
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
    except Exception:
        return None
    return None


class JobsChProvider(BaseJobProvider):
    name: str = "jobs.ch"
    SEARCH_URL: str = "https://www.jobs.ch/api/v1/public/search"
    DETAIL_URL: str = "https://www.jobs.ch/api/v1/public/search/job/{job_id}"

    def search(self, target_roles: List[str], location: str) -> List[JobItem]:
        items: List[JobItem] = []
        seen_ids = set()
        source_cfg = self.config.get("sources", {}).get("jobsch", {})
        max_pages = source_cfg.get("max_pages", 4)

        for role in target_roles:
            query = f"{role} {location}"
            for page in range(1, max_pages + 1):
                params = {
                    "query": query,
                    "rows": 20,
                    "page": page
                }
                res = fetch_json(self.SEARCH_URL, params=params)
                if not res or "documents" not in res:
                    break
                docs = res.get("documents", [])
                if not docs:
                    break

                for doc in docs:
                    raw_id = doc.get("job_id")
                    if not raw_id or raw_id in seen_ids:
                        continue
                    seen_ids.add(raw_id)

                    company = " ".join(doc.get("company_name", "Unbekannt").split())
                    title = " ".join(doc.get("title", "").split())
                    place = " ".join(doc.get("place", "").split())
                    preview = doc.get("preview", "") or ""
                    pub_date = (doc.get("publication_date", "") or "")[:10]
                    job_url = f"https://www.jobs.ch/de/stellenangebote/detail/{raw_id}/"

                    item = JobItem(
                        source=self.name,
                        id=f"jobsch:{raw_id}",
                        title=title,
                        company=company,
                        place=place,
                        date=pub_date,
                        url=job_url,
                        preview=preview,
                        skills=doc.get("skills") or []
                    )
                    items.append(item)

                if len(docs) < 20:
                    break

        return items

    def fetch_full_text(self, job_id: str) -> Optional[Dict[str, Any]]:
        clean_id = job_id.replace("jobsch:", "").strip()
        url = self.DETAIL_URL.format(job_id=clean_id)
        data = fetch_json(url)
        if not data:
            return None

        title = data.get("title", "Stellenangebot")
        company = data.get("company_name", "Unternehmen")
        place = data.get("place", "Zürich")
        pub_date = (data.get("publication_date", "") or "")[:10]
        job_url = f"https://www.jobs.ch/de/stellenangebote/detail/{clean_id}/"
        template = data.get("template", "")
        description_text = clean_html(template) if template else data.get("preview", "")
        skills_list = data.get("skills", []) or []

        return {
            "title": title,
            "company": company,
            "place": place,
            "date": pub_date,
            "url": job_url,
            "id": f"jobsch:{clean_id}",
            "description": description_text,
            "skills": skills_list
        }
