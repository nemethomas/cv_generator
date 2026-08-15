---
description: Prüft alle Hyperlinks, URLs und E-Mail-Adressen im PDF-Lebenslauf auf Erreichbarkeit (Status 200, 404, Redirects).
---

Führe eine automatisierte Prüfung aller Links und E-Mail-Adressen in den Lebenslauf-PDFs gemäss dem Skill `links` durch.

**Ziel:**
- Falls ein Argument übergeben wurde (z. B. `$ARGUMENTS` wie `adcubum` oder `standard`), prüfe das entsprechende PDF in `dist/`.
- Falls kein Argument angegeben ist, prüfe alle PDFs in `dist/`.

**Ausführung:**
Führe das Prüfskript `python3 skills/links/check_links.py "$ARGUMENTS"` aus und gib den strukturierten Bericht mit Status-Ampel aus.
