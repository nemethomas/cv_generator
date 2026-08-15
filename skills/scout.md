# Skill: scout (Job Scouting & Evidence Matcher)

Durchsucht Schweizer Stellenportale (jobs.ch API) nach passenden IT- und Business-Engineering-Positionen im Grossraum Zürich, filtert nach Blacklist (RUAG) und Whitelist (Swisscom, ZKB, Google, Zühlke, Inventx) und bewertet den Match-Score anhand der Arbeitszeugnisse in `docs/`.

## Aufruf

- In der CLI: `/scout` (Standard-Suche nach Top-Matches im Raum Zürich)
- Gezielte Suche: `/scout "Data Scientist"`, `/scout "SYRIUS"`, `/scout "Business Engineer"`
- Whitelist-Fokus: `/scout --whitelist`
- URL-Analyse: `/scout <jobs.ch-url>`
