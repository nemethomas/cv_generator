---
description: Schneller Trust- & Evidence-Check des Lebenslaufs gegen die Nachweise in docs/ (Scores, Gaps & Risiken).
---

Führe ein schnelles und fokussiertes Trust- & Evidence-Audit gemäss dem Skill `audit` durch.

**Ziel-Datei:**
- Falls ein Argument übergeben wurde (z. B. `/audit adcubum` oder `/audit src/cv-adcubum.md`), prüfe diese Datei.
- Falls kein Argument angegeben ist, prüfe standardmässig `src/cv-adcubum.md`.

**Vorgehen (zielgerichtet & schnell):**
1. Gleiche die Lebenslauf-Stationen und Bildungsabschlüsse mit den Dateinamen in `docs/` ab.
2. Lies gezielt nur die relevanten Zeugnisse aus `docs/zeugnisse/` ein, um Zeit und Ressourcen zu sparen.
3. Berechne die 4 Teil-Scores ($T, A, F, P$) und den Gesamt-Trust-Score.
4. Gib einen kompakten Bericht aus:
   - **Executive Summary & Trust-Score**
   - **Kompakte Stationen- & Belegübersicht**
   - **Gaps & Diskrepanzen** (Fokus auf ⚠️, 🔴 und unklare Punkte) mit konkreten Handlungsempfehlungen.
