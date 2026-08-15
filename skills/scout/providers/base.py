#!/usr/bin/env python3
"""
Base classes and data models for job search providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class JobItem:
    """Normalized job posting representation across all providers."""
    source: str                          # e.g., "jobs.ch", "linkedin", "indeed", "swissdevjobs"
    id: str                              # Unique ID across provider (e.g. "jobsch:123", "li:456")
    title: str                           # Job title
    company: str                         # Company name
    place: str                           # Location / City
    date: str                            # ISO date YYYY-MM-DD
    url: str                             # Original job URL
    preview: str                         # Summary or description snippet
    description_full: Optional[str] = None # Full text if available
    skills: List[str] = field(default_factory=list) # Extracted skills / tags
    is_whitelist: bool = False
    whitelist_name: Optional[str] = None
    match_score: int = 0
    matched_keywords: List[str] = field(default_factory=list)


class BaseJobProvider(ABC):
    """Abstract interface that every job search provider must implement."""
    name: str = "base"

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def search(self, target_roles: List[str], location: str) -> List[JobItem]:
        """Search vacancies for the given roles and location."""
        pass

    @abstractmethod
    def fetch_full_text(self, job_id: str) -> Optional[str]:
        """Fetch full description text for a job ID."""
        pass
