# Skill: test (Ganzheitlicher QA-Workflow)

Orchestriert eine vollständige Qualitätsprüfung des Lebenslaufs über 4 Prüfdimensionen und liefert eine kompakte Zusammenfassung aller Ergebnisse mit Status-Ampel.

## Aufgerufene Module
1. `fit` – Stellen-Fit & Match-Score gegen Inserate in `jobs/`
2. `audit` – Trust- & Beleg-Check gegen Nachweise in `docs/`
3. `spell` – Rechtschreib-, Grammatik- & Schweizer Orthografie-Prüfung
4. `links` – Validierung aller Hyperlinks & E-Mail-Adressen in `dist/*.pdf`

## Aufruf
- `/test` (Standard: `adcubum`)
- `/test adcubum`
- `/test standard`
