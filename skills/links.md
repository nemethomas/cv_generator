# Skill: links (PDF & CV Link Checker)

Prüft alle Hyperlinks, URLs und E-Mail-Adressen in den kompilierten PDF-Dateien in `dist/` und den Markdown-Quellen in `src/` auf Erreichbarkeit, Statuscodes und Gültigkeit.

## Aufruf
- In der CLI: `/links` (prüft alle PDFs) oder `/links <name>` (z. B. `/links adcubum`, `/links standard`).
- Direkt über Python: `python3 skills/links/check_links.py [target]`
