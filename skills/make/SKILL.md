---
name: make
description: Kompiliert Lebenslauf-Markdown-Dateien (src/cv-*.md) mittels Pandoc und XeLaTeX mit der Vorlage templates/cv-template.tex in druckfertige PDF-Dokumente unter dist/ und öffnet das fertige PDF direkt in der Vorschau.
---

# Skill: PDF-Kompilierung & Vorschau (make)

Dieser Skill übernimmt das automatisierte Bauen und Kompilieren von Lebensläufen (`src/cv-*.md`) und Motivationsschreiben (`src/letter-*.md`) in hochwertige PDFs (`dist/cv-*.pdf`, `dist/letter-*.pdf`) unter Verwendung von Pandoc, XeLaTeX und den Templates `templates/cv-template.tex` bzw. `templates/letter-template.tex` sowie das anschliessende Öffnen in der macOS-Vorschau.

## Ablauf

1. **PDF generieren** mit Pandoc & XeLaTeX.
2. **PDF direkt in Vorschau öffnen** via macOS `open`.

## Kompilierungsbefehle

### 1. Einzelne Dokumente kompilieren & öffnen

```bash
# Lebenslauf kompilieren
pandoc src/cv-<target>.md \
  --template=templates/cv-template.tex \
  --pdf-engine=xelatex \
  --shift-heading-level-by=-1 \
  -o dist/cv-<target>.pdf && open dist/cv-<target>.pdf

# Motivationsschreiben kompilieren
pandoc src/letter-<target>.md \
  --template=templates/letter-template.tex \
  --pdf-engine=xelatex \
  -o dist/letter-<target>.pdf && open dist/letter-<target>.pdf
```

## Parameter & Optionen

- `adcubum` (Standard): Baut und öffnet `dist/cv-adcubum.pdf` und `dist/letter-adcubum.pdf`
- `cv-adcubum`: Baut und öffnet nur den Lebenslauf `dist/cv-adcubum.pdf`
- `letter-adcubum`: Baut und öffnet nur das Anschreiben `dist/letter-adcubum.pdf`
- `standard`: Baut und öffnet `dist/cv-standard.pdf` aus `src/cv-standard.md`
- `all`: Kompiliert alle vorhandenen Dokumente in `src/*.md` und öffnet sie

