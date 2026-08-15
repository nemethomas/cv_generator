# Skill: make (PDF-Kompilierung & Vorschau)

Kompiliert Markdown-Lebensläufe (`src/cv-*.md`) und Motivationsschreiben (`src/letter-*.md`) mittels Pandoc und XeLaTeX mit den Vorlagen `templates/cv-template.tex` bzw. `templates/letter-template.tex` in druckfertige PDF-Dateien unter `dist/` und öffnet diese anschliessend automatisch in der macOS-Vorschau.

## Aufruf
- In der CLI: `/make adcubum`, `/make letter-adcubum`, `/make standard` oder `/make all`
- Ausführung:
  ```bash
  pandoc src/cv-adcubum.md \
    --template=templates/cv-template.tex \
    --pdf-engine=xelatex \
    --shift-heading-level-by=-1 \
    -o dist/cv-adcubum.pdf && open dist/cv-adcubum.pdf
  ```

