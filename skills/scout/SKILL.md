---
name: scout
description: Durchsucht Schweizer Stellenportale (jobs.ch API, LinkedIn/Indeed via JobSpy, SwissDevJobs) nach passenden Positionen im Grossraum Zürich, filtert nach Blacklist (RUAG), prüft den Pensum-Filter (>= 60%) und berechnet einen dynamischen Evidence-Match-Score anhand der Arbeitszeugnisse und des Profils (docs/profile.json).
---

# Skill: Job Scout & Evidence Matcher (scout)

Dieser Skill automatisiert die Multi-Source-Suche, Filterung und Bewertung passender Stellenangebote im Grossraum Zürich über mehrere Portale (jobs.ch, LinkedIn, Indeed, SwissDevJobs) auf Basis deines dynamischen Leistungsprofils und deiner Arbeitszeugnisse in `docs/profile.json`.

---

## 📡 Unterstützte Quellen (Provider-Architektur)

1. **`jobs.ch` (JobCloud API):** Direkte, tagesaktuelle Schweizer Unternehmensabdeckung (Banken, Versicherungen, Behörden, KMUs).
2. **`JobSpy` (LinkedIn, Indeed, Glassdoor):** Moderne Tech- & Data-Rollen, Scale-ups und internationale Konzerne.
3. **`SwissDevJobs`:** Spezialisierter Schweizer Tech- & Entwickler-Feed.

Die Quellen können in `skills/scout/config.json` modular aktiviert oder deaktiviert werden.

---

## 🎯 Suchkriterien & Filter

1. **Standort & Region:**
   - **Fokus:** Zürich und unmittelbare Agglomeration (`Zürich`, `Altstetten`, `Dietikon`, `Dübendorf`, `Wallisellen`).
2. **Pensum:**
   - Mindestens **60 %** (60–100 %).
3. **Dynamische Zielrollen (`docs/profile.json`):**
   - Werden beim Ausführen von `make dossier` vollautomatisch aus den Zeugnissen und dem Lebenslauf extrahiert.
4. **Blacklist-Unternehmen (🚫 Kategorischer Ausschluss):**
   - **RUAG** (inkl. aller Sparten wie MRO, Defence, Space).

---

## 📊 Bewertungsmatrix (Evidence Match Score 0–100%)

Jede gefundene Stelle wird dynamisch gegen deine realen Nachweise in `docs/profile.json` bewertet:

| Kriterium | Gewicht | Prüfung gegen `docs/profile.json` |
| :--- | :---: | :--- |
| **Tech- & Domain-Stack** | **40 %** | Dynamische Keyword-Wortwolke aus den Zeugnissen (mit Häufigkeitsgewichtung). |
| **Rollen- & Aufgaben-Fit** | **40 %** | Übereinstimmung mit deinen extrahierten Berufsbezeichnungen und Funktionen. |
| **Ausbildung & Zertifikate** | **20 %** | Bestätigte Abschlüsse und Zertifikate aus `docs/`. |

---

## 🚀 CLI-Verwendung

```bash
# Standard-Suche: Top-Matches im Raum Zürich (oder im Terminal: make scout)
/scout

# Gezielte Suche nach einer Rolle oder Technologie
/scout "Data Scientist"
/scout "SYRIUS"

# Nur Whitelist-Unternehmen durchsuchen
/scout --whitelist

# Gefundenes Inserat mit kurzem Firmenkürzel in jobs/ anlegen
python3 skills/scout/search_jobs.py --save <job-id> --as <firma>
```

---

## 🔄 Nahtloser Workflow nach dem Scouting

1. **Stelle importieren:** Das Inserat wird mit `--save <id> --as <firma>` sauber als `jobs/<firma>.md` (z. B. `jobs/zkb.md`) abgelegt.
2. **Passgenauigkeit vertiefen:** `/fit <firma>` analysiert den genauen Match und ATS-Keywords.
3. **Bewerbungsunterlagen bauen:** `make <firma>` generiert den massgeschneiderten 2-Seiter und das Anschreiben.
