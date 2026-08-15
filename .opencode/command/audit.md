---
description: Schneller Trust- & Evidence-Check des Lebenslaufs gegen die Nachweise in docs/ (Scores, Gaps & Risiken).
---

Führe ein schnelles und fokussiertes Trust- & Evidence-Audit gemäss dem Skill `audit` durch.

**Sonderbefehl:**
- Falls "$ARGUMENTS" gleich `sync` oder `import` ist, führe `python3 skills/audit/sync_dossier.py` aus, um alle PDFs in `docs/` neu einzulesen und `docs/dossier.md` zu aktualisieren.

**Ziel-Datei für Audit:**
- Falls ein Argument übergeben wurde (z. B. `/audit example` oder `/audit src/cv-example.md`), prüfe diese Datei.
- Falls kein Argument angegeben ist, prüfe standardmässig `src/cv-example.md`.

**Vorgehen:**
1. Lade das zentrale Dossier aus `docs/dossier.md` (oder synchronisiere via `sync_dossier.py`, falls noch nicht vorhanden).
2. Gleiche Lebenslauf-Stationen, Verantwortungen und Bildungsabschlüsse direkt mit den Volltext-Transkripten ab.
3. Berechne die 4 Teil-Scores ($T, A, F, P$) und den Gesamt-Trust-Score.
4. Gib einen kompakten Bericht aus:
   - **Executive Summary & Trust-Score**
   - **Kompakte Stationen- & Belegübersicht**
   - **Gaps & Diskrepanzen** mit konkreten Handlungsempfehlungen.
