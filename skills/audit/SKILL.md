---
name: audit
description: Schneller und präziser Trust- & Evidence-Check (Score 0-100%) eines Lebenslaufs (src/*.md) anhand der Nachweise in docs/. Prüft gezielt Stationen, Zeugnisse und Zertifikate und liefert eine kompakte Gap- & Diskrepanzanalyse.
---

# Skill: CV Trust & Evidence Auditor (audit)

Dieser Skill prüft die Belastbarkeit, Belegbarkeit und Glaubwürdigkeit von Angaben im Lebenslauf (`src/*.md`) anhand der im Dossier (`docs/`) hinterlegten Zeugnisse, Zertifikate und Diplome – **schnell, zielgerichtet und fokussiert auf Abweichungen & Risiken**.

## Bewertungsdimensionen & Berechnungsmatrix

$$\text{Trust-Score} = (T \times 0.25) + (A \times 0.25) + (F \times 0.30) + (P \times 0.20)$$

1. **Timeline & Stationen ($T$ – 25 %):** Übereinstimmung von Arbeitgebern, Titeln und Zeiträumen mit den Arbeitszeugnissen.
2. **Aus- & Weiterbildung / Zertifikate ($A$ – 25 %):** Nachweis aller genannten Bildungsabschlüsse (CAS, Diplome, EFZ) und Zertifikate (IREB, IPMA, ITIL).
3. **Fachliche Aufgaben & Verantwortung ($F$ – 30 %):** Bestätigung von Kernsystemen (SYRIUS, OMS/DMS, IAM, Migration) und Verantwortungen in den Zeugnissen.
4. **IT-Skills, Methoden & Projekte ($P$ – 20 %):** Nachvollziehbarkeit technischer Skills, Rollen und Methoden.

---

## Performance-optimierter Workflow

Um die Analyse schnell und ressourcenschonend durchzuführen:

1. **Ziel-Lebenslauf identifizieren:**
   - Standardmässig **eine** Zieldatei prüfen (angegebenes Argument, z. B. `src/cv-adcubum.md` oder `src/cv-standard.md`). Nicht mehrere CVs gleichzeitig prüfen, ausser explizit verlangt.

2. **Gezielte Dateiauswahl (Targeted / On-Demand Loading):**
   - **Nicht** alle 20+ PDFs blind einlesen!
   - **Dateinamen-Mapping nutzen:** Diplome und Zertifikate (`docs/ausbildung/`, `docs/zertifikate/`, `docs/sprachen/`) sind anhand der Dateinamen direkt verifizierbar (z. B. `2024_CAS_Data_Engineering_Zertifikat.pdf`, `IREB_Requirements_Engineering.pdf`).
   - **Arbeitszeugnisse gezielt öffnen:** Nur die für die jeweiligen Arbeitgeber relevanten Zeugnisse aus `docs/zeugnisse/` einlesen (z. B. für Swisscom nur `2026_Swisscom_Arbeitszeugnis.pdf`).

3. **Exception-Driven Reporting (Fokus auf Relevantes):**
   - Statt 50+ Zeilen für jede unstrittige Einzelaussage auszugeben, konzentriert sich der Bericht auf Scores, Bestätigungen und **konkrete Diskrepanzen/Gaps**.

---

## Ausgabeformat

### 1. Executive Summary
- **Gesamt-Trust-Score (in %)** mit Ampel (🟢 90–100% Exzellent, 🟡 75–89% Gut, 🔴 <75% Kritisch).
- Teil-Scores: $T$, $A$, $F$, $P$.

### 2. Stationen- & Zertifikate-Schnellübersicht (Kompakttabelle)
Kompakte Zeilenübersicht: *Station/Abschluss | Zeitraum | Belegdokument | Status (🟢/🟡/🔴/⚠️)*.

### 3. Gaps, Diskrepanzen & Prüfhinweise (Fokus)
Auflistung **nur** der Punkte mit Abweichungen oder fehlenden Nachweisen (⚠️ Diskrepanz, 🔴 Unbelegt, 🟡 Teilweise belegt) mit:
- *CV-Aussage*
- *Befund / Zeugnis-Auszug*
- *Risikobewertung fürs Interview*
- *Konkreter Formulierungsvorschlag zur Entschärfung*

*(Optional: Bei Aufruf `/audit full` oder `/audit detailed` wird die vollständige Einzel-Bullet-Point-Matrix ausgegeben).*
