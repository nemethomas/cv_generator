---
name: fit
description: Berechnet und analysiert den Erfüllungsgrad (Match-Score 0-100%) zwischen einem Stellenbeschrieb (Job Posting unter jobs/) und dem Lebenslauf (src/*.md bzw. dist/*.pdf) anhand einer 4-dimensionalen Bewertungsmatrix, Soll-Ist-Gegenüberstellung, ATS-Keyword-Prüfung und konkreten Optimierungsvorschlägen.
---

# Skill: Fit & Match-Score Analyzer

Dieser Skill misst und analysiert den Erfüllungsgrad zwischen einer Stellenausschreibung (in `jobs/`) und dem entsprechenden Lebenslauf (`src/*.md` bzw. `dist/*.pdf`).

## Bewertungsdimensionen & Berechnungsformel

Der Gesamt-Erfüllungsgrad wird nach einer gewichteten 4-Säulen-Matrix berechnet:

$$\text{Gesamt-Score} = (M \times 0.40) + (N \times 0.25) + (R \times 0.20) + (K \times 0.15)$$

### 1. Must-Have Anforderungen ($M$ – Gewicht: 40 %)
- **Kriterien:** Ausbildung/Studium, zwingende Kerntechnologien (z. B. Oracle, SQL, PL/SQL, Scripting), zwingende Sprachkenntnisse, verlangte Kern-Berufserfahrung.
- **Bewertungsskala:**
  - 🟢 **100 % (Voll erfüllt):** Explizit im CV mit konkreter Praxis/Station belegt.
  - 🟡 **50 % (Teilweise / Implizit):** Grundwissen vorhanden oder nur implizit erkennbar.
  - 🔴 **0 % (Nicht belegt):** Im Lebenslauf nicht ersichtlich.

### 2. «Von Vorteil» & Nice-to-Have ($N$ – Gewicht: 25 %)
- **Kriterien:** Spezialisierte Tools (z. B. SYRIUS-Parametrierung, MDB-Schnittstelle), Fachdomänen (z. B. Krankenversicherungs-Leistungen, KVG/VVG/UVG, Sachschaden, Vertragsverwaltung), optionale Sprachen (z. B. Französisch), Python/VBA.
- **Bewertungsskala:**
  - 🟢 **100 %:** Voll nachgewiesen.
  - 🟡 **50 %:** Grundkenntnisse vorhanden.
  - 🔴 **0 %:** Fehlt.

### 3. Rollen-, Methoden- & Praxis-Fit ($R$ – Gewicht: 20 %)
- **Kriterien:** Requirements Engineering, Spezifikationen, Use Cases, Workshop-Leitung/Moderation, Kundenkontakt, Troubleshooting & Fehleranalyse, IAM-Verständnis.
- **Bewertungsskala:**
  - 🟢 **100 %:** Mit konkreten Aufgaben und Resultaten beschrieben.
  - 🟡 **50 %:** Nur als Stichwort gelistet ohne Projektkontext.
  - 🔴 **0 %:** Nicht erwähnt.

### 4. ATS & Keyword-Abdeckung ($K$ – Gewicht: 15 %)
- **Kriterien:** Exakte Übereinstimmung der Schlüsselwörter aus dem Stelleninserat im CV (z. B. PL/SQL, Oracle, MDB, Parametrierung, Use Cases, Migration, DMS, OMS, IAM).
- **Berechnung:** $\frac{\text{Gefundene Keywords}}{\text{Relevante Keywords im Inserat}} \times 100\,\%$

---

## Workflow bei der Analyse

1. **Eingabedateien laden:**
   - Stellenbeschrieb aus `jobs/<name>.md` (oder übergebenes Inserat)
   - Lebenslauf-Quelle aus `src/cv-<name>.md` und prüfen gegen das kompilierte PDF in `dist/`
2. **Kriterien extrahieren & bewerten:**
   - Alle Anforderungen in die 4 Dimensionen aufteilen und einzeln mit 🟢/🟡/🔴 bewerten.
3. **Score berechnen:**
   - Berechnung der Teil-Scores und des gewichteten Gesamt-Scores.
4. **Bericht generieren:**
   - **Executive Summary:** Gesamt-Score mit farblicher Ampel & Fazit.
   - **Soll-Ist-Vergleichstabelle:** Gegenüberstellung aller Punkte inkl. Fundstelle im CV.
   - **Gap-Analyse:** Identifizierte Lücken oder ungenutzte Potenziale.
   - **Konkrete Text-Optimierungen:** Formulierungsvorschläge für `src/*.md`, um den Match auf 95%+ zu heben.
