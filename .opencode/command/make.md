---
description: Kompiliert Lebenslauf- und Motivationsschreiben-Markdown-Dateien in PDFs unter dist/ und öffnet sie in der macOS-Vorschau.
---

Kompiliere die Dokumente für "$ARGUMENTS" gemäss dem Skill `make`.

**Ziel:**
- Falls `$ARGUMENTS` angegeben ist (z. B. `example`, `letter-example`, `cv-example`):
  Führe `make $ARGUMENTS` aus und öffne die entsprechenden PDFs in `dist/`.
- Falls `$ARGUMENTS` gleich `all` ist:
  Führe `make all` aus und öffne alle generierten PDFs.
- Falls kein Argument angegeben ist:
  Kompiliere standardmässig `example` (`make example`).

**Befehl zur Kompilierung:**
```bash
make $ARGUMENTS
```
