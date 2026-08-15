# Skill: audit (CV Trust & Evidence Auditor)

Prüft die Glaubwürdigkeit und Belegbarkeit eines Lebenslaufs in `src/` anhand der hinterlegten Nachweise im Dossier `docs/` (schnell, ressourceneffizient und fokussiert auf Risiken & Gaps).

## Berechnungsmatrix

$$\text{Trust-Score} = (T \times 0.25) + (A \times 0.25) + (F \times 0.30) + (P \times 0.20)$$

- **25 % Timeline ($T$):** Exakte Übereinstimmung von Arbeitgebern, Titeln und Zeiträumen mit Arbeitszeugnissen.
- **25 % Aus- & Weiterbildung ($A$):** Nachweis aller Abschlüsse, CAS, Diplome und Fachzertifikate.
- **30 % Fachliche Aufgaben ($F$):** Bestätigung der Rollen, Kernsysteme (SYRIUS, OMS/DMS, IAM, Migration) und Verantwortungen in den Zeugnissen.
- **20 % Skills & Projekte ($P$):** Nachweisbarkeit von IT-Skills, Tools und Projektergebnissen.

## Aufruf
- In der CLI: `/audit` (prüft Standard-Lebenslauf `src/cv-example.md`) oder `/audit <name>`.
- Tiefenprüfung: `/audit full` oder `/audit <name> full`.
