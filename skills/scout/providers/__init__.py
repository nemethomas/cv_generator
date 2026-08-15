#!/usr/bin/env python3
"""
Provider Registry & Dispatcher for Job Scout.
"""

from typing import List, Optional, Dict, Any

from .base import BaseJobProvider, JobItem
from .jobsch import JobsChProvider
from .jobspy import JobSpyProvider
from .swissdevjobs import SwissDevJobsProvider

PROVIDER_CLASSES = {
    "jobsch": JobsChProvider,
    "jobspy": JobSpyProvider,
    "swissdevjobs": SwissDevJobsProvider
}


def get_enabled_providers(config: Dict[str, Any]) -> List[BaseJobProvider]:
    """Instantiate and return all active job providers based on config.json."""
    sources_cfg = config.get("sources", {})
    providers = []

    for key, provider_cls in PROVIDER_CLASSES.items():
        src_info = sources_cfg.get(key, {})
        # If sources not explicitly configured, enable jobsch and swissdevjobs by default
        is_enabled = src_info.get("enabled", True) if sources_cfg else (key in ["jobsch", "swissdevjobs"])
        if is_enabled:
            providers.append(provider_cls(config))

    return providers


def fetch_full_job_data(job_id: str, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Retrieve full job details using the corresponding provider."""
    # Check ID prefix first
    prefix = job_id.split(":")[0].lower() if ":" in job_id else "jobsch"

    prefix_map = {
        "jobsch": JobsChProvider,
        "linkedin": JobSpyProvider,
        "indeed": JobSpyProvider,
        "glassdoor": JobSpyProvider,
        "jobspy": JobSpyProvider,
        "sdj": SwissDevJobsProvider
    }

    target_cls = prefix_map.get(prefix)
    if target_cls:
        provider = target_cls(config)
        res = provider.fetch_full_text(job_id)
        if res:
            return res

    # Fallback: query all providers
    for provider in get_enabled_providers(config):
        res = provider.fetch_full_text(job_id)
        if res:
            return res

    return None
