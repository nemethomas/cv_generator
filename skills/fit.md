# Skill: fit (Match-Score & Erfüllungsgrad)

Analysiert die Übereinstimmung zwischen einer Stellenausschreibung in `jobs/` und einem Lebenslauf in `src/`.

## Berechnungsmatrix

$$\text{Gesamt-Score} = (M \times 0.40) + (N \times 0.25) + (R \times 0.20) + (K \times 0.15)$$

- **40 % Must-Have ($M$):** Ausbildung, Kern-IT-Skills (SQL, PL/SQL, Oracle, Scripting), zwingende Sprachen, Kern-Erfahrung.
- **25 % Nice-to-Have ($N$):** Branchen- & Toolwissen (SYRIUS, MDB, Parametrierung, Leistungen, KVG/UVG, Französisch).
- **20 % Rollen-Fit ($R$):** Requirements Engineering, Use Cases, Workshop-Moderation, Troubleshooting, IAM.
- **15 % ATS & Keywords ($K$):** Direkte Keyword-Trefferquote der Kernbegriffe aus dem Inserat.

## Aufruf
- In der CLI: `/fit` (prüft das aktuellste Jobinserat) oder `/fit <name>` (z. B. `/fit example`).
