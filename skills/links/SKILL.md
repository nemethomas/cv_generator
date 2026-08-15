---
name: links
description: Prüft alle Hyperlinks, E-Mail-Adressen und URLs in den generierten PDF-Dateien (dist/*.pdf) und Quell-Markdown-Dateien (src/*.md) auf Erreichbarkeit (HTTP 200, Redirects, 404 Fehler) und korrekte Verlinkung.
---

# Skill: PDF & CV Link Checker (links)

Dieser Skill prüft automatisiert alle im PDF (`dist/*.pdf`) und in den Quelltexten (`src/*.md`) eingebetteten Hyperlinks, E-Mail-Adressen, Social-Media-Profile und Projekt-Repositories auf ihre Gültigkeit, Erreichbarkeit und syntaktische Korrektheit.

## Prüfungsdimensionen

1. **PDF-Annotationen & Hyperlinks:**
   - Extraktion aller `/URI`-Links aus den PDF-Seiten mittels `pypdf` bzw. `skills/links/check_links.py`.
2. **HTTP- & HTTPS-Erreichbarkeit:**
   - **🟢 200 OK / 30x Redirect:** Zieladresse ist live und liefert fehlerfreien Inhalt.
   - **🟡 Protected / Bot-Schutz:** HTTP 403 / 999 (z. B. LinkedIn-Login-Schutz oder Cloudflare-Challenge bei Medium) – Domain existiert, URL ist syntaktisch korrekt.
   - **🔴 404 Not Found / Dead Link:** Toter Link oder gelöschtes Repository.
   - **🔴 Verbindungsfehler / DNS-Timeout:** Domain existiert nicht oder Server reagiert nicht.
3. **E-Mail- & Kontaktdaten-Validierung:**
   - `mailto:`-Formatprüfung (gültige Syntax wie `name@domain.tld`).
4. **Konsistenz zwischen Anzeigetext & Linkziel:**
   - Stimmt der angezeigte Text im Lebenslauf (z. B. `github.com/nemethomas/sam`) mit der tatsächlich hinterlegten Ziel-URL überein?

---

## Workflow

1. **Prüfung ausführen:**
   - Entweder über das integrierte Prüfskript:
     ```bash
     python3 skills/links/check_links.py [adcubum | standard | all]
     ```
   - Oder direkt durch Analyse der Markdown-Dateien `src/*.md` und PDF-Dateien `dist/*.pdf`.

2. **Ergebnisbericht ausgeben:**
   - **Übersicht nach PDF-Datei und Seite**
   - **Status-Ampel (🟢 / 🟡 / 🔴)**
   - **Konkrete Warnungen oder Korrekturempfehlungen** bei toten URLs oder fehlerhaften Weiterleitungen.

---

## CLI-Aufruf

- `/links` (prüft alle PDFs in `dist/`)
- `/links adcubum` (prüft gezielt `dist/adcubum.pdf`)
- `/links standard` (prüft gezielt `dist/standard.pdf`)
