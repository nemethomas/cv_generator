---
name: scout
description: Durchsucht Schweizer Stellenportale (jobs.ch API) sowie Karriereportale nach passenden IT-, Business-Engineering- und Data-Science-Positionen im Grossraum Zürich, filtert nach Blacklist (RUAG) und Whitelist (Swisscom, ZKB, Google, Zühlke, Inventx), prüft den Pensum-Filter (>= 60%) und berechnet einen Evidence-Match-Score anhand der Arbeitszeugnisse und des Profils.
---

# Skill: Job Scout & Evidence Matcher (scout)

Dieser Skill automatisiert die Suche, Filterung und Bewertung passender Stellenangebote im Grossraum Zürich auf Basis deines echten Leistungsprofils und deiner Arbeitszeugnisse in `docs/`.

---

## 🎯 Suchkriterien & Filter

1. **Standort & Region:**
   - **Fokus:** Zürich und unmittelbare Agglomeration (`Zürich`, `Altstetten`, `Dietikon`, `Dübendorf`, `Wallisellen`).
2. **Pensum:**
   - Mindestens **60 %** (60–100 %).
3. **Zielrollen:**
   - *Business Engineer, Requirements Engineer, IT Business Analyst, Solution Designer, Data Engineer, Data Scientist, Product Owner, Technical Consultant*.
4. **Whitelist-Unternehmen (⭐ Priorisiert mit +15 % Bonus):**
   - **Swisscom**
   - **Zürcher Kantonalbank (ZKB)**
   - **Google Switzerland**
   - **Zühlke Informatik**
   - **Inventx**
   - **Migros** (inkl. MGB, Migros Bank, Migros IT Services)
5. **Blacklist-Unternehmen (🚫 Kategorischer Ausschluss):**
   - **RUAG** (inkl. aller Sparten wie MRO, Defence, Space).

---

## 📊 Bewertungsmatrix (Evidence Match Score 0–100%)

Jede gefundene Stelle wird gegen deine realen Nachweise und Zeugnisse bewertet:

| Kriterium | Gewicht | Prüfung gegen `docs/` & Profil |
| :--- | :---: | :--- |
| **Tech- & Domain-Stack** | **40 %** | Praxisnachweis in Zeugnissen (SQL, Oracle, PL/SQL, Python, SYRIUS, Data Engineering, Data Science, Machine Learning, ETL, DWH, IAM, Berechtigungen). |
| **Rollen- & Aufgaben-Fit** | **35 %** | Übereinstimmung mit Aufgaben (Business Engineering, Requirements Engineering, BPMN, Use Cases, Migration, Solution Design). |
| **Ausbildung & Diplome** | **10 %** | Bestätigte Abschlüsse (CAS Data Engineering, CAS Business Analysis, CAS Projektmanagement, IREB, IPMA, ITIL, EFZ/Maturität). |
| **Whitelist-Bonus** | **15 %** | **+15 %** für Stellen bei *Swisscom, ZKB, Google, Zühlke Informatik, Inventx*. |

---

## 🚀 CLI-Verwendung

```bash
# Standard-Suche: Top-Matches im Raum Zürich
/scout

# Gezielte Suche nach einer Rolle oder Technologie
/scout "Data Scientist"
/scout "SYRIUS"

# Nur Whitelist-Unternehmen durchsuchen
/scout --whitelist

# Einzelne Stellen-URL analysieren und nach jobs/ exportieren
/scout https://www.jobs.ch/de/stellenangebote/detail/<id>/

# Gefundenes Inserat herunterladen und in jobs/ anlegen
python3 skills/scout/search_jobs.py --save <job-id>
```

---

## 🔄 Nahtloser Workflow nach dem Scouting

1. **Stelle importieren:** Das Inserat wird mit `--save <id>` sauber als `jobs/<firma>-<titel>.md` abgelegt.
2. **Passgenauigkeit vertiefen:** `/fit <firma>` analysiert den genauen Match und ATS-Keywords.
3. **Bewerbungsunterlagen bauen:** `make <firma>` generiert den massgeschneiderten 2-Seiter und das Anschreiben.
