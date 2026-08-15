---
description: Berechnet den Erfüllungsgrad (Match-Score) zwischen einem Stellenbeschrieb in jobs/ und dem CV in src/.
---

Führe eine strukturierte Fit-Analyse gemäss dem Skill `fit` durch.

Prüfe den Stellenbeschrieb für "$ARGUMENTS" (falls kein Argument angegeben ist, nimm die Datei aus `jobs/`, z.B. `jobs/adcubum.md`) gegen den entsprechenden Lebenslauf in `src/` (z.B. `src/cv-adcubum.md`).

Berechne den Erfüllungsgrad nach der 4-Säulen-Matrix:
1. Must-Have Anforderungen (40 %)
2. Nice-to-Have / Von Vorteil (25 %)
3. Rollen-, Methoden- & Praxis-Fit (20 %)
4. ATS- & Keyword-Abdeckung (15 %)

Gib den Bericht strukturiert aus:
- Gesamt-Erfüllungsgrad in % (mit Ampel)
- Detaillierte Soll-Ist-Tabelle (Anforderung | Belegstelle im CV | Status)
- Gap-Analyse
- Konkrete Handlungsempfehlungen zur Steigerung des Scores
