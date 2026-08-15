# CV & Application Management

Strukturierte Verwaltung, Qualitätssicherung und automatisierte Erstellung von massgeschneiderten Lebensläufen und Motivationsschreiben mit Markdown, Pandoc und XeLaTeX.

Der Inhalt wird modular in Markdown gepflegt, während Layout, Farben, Typografie und Foto-Position getrennt über wiederverwendbare LaTeX-Templates gesteuert werden.

---

## Funktionsweise

```
src/cv-<firma>.md                 src/letter-<firma>.md
        │                                   │
        ▼                                   ▼
Pandoc + templates/cv-template.tex   Pandoc + templates/letter-template.tex
        │                                   │
        ▼                                   ▼
     XeLaTeX                             XeLaTeX
        │                                   │
        ▼                                   ▼
dist/cv-<firma>.pdf                 dist/letter-<firma>.pdf
```

- **Markdown (`src/`)**: Enthält die reinen Textinhalte, getrennt für Lebenslauf (`cv-*.md`) und Motivationsschreiben (`letter-*.md`).
- **LaTeX-Templates (`templates/`)**: Definieren das visuelle Erscheinungsbild (Layout, Spalten, Farben, Schriftarten, Icons und Foto-Position).
- **Pandoc**: Überträgt die Inhalte und Metadaten aus den Markdown-Dateien in die LaTeX-Templates.
- **XeLaTeX**: Kompiliert das finale Dokument als druckfertiges, hochauflösendes PDF.

Dadurch lassen sich Inhalt und Gestaltung vollständig unabhängig voneinander pflegen.

---

## Projektstruktur

```text
.
├── assets/
│   ├── fonts/               # Schriftarten (z. B. Inter OTF)
│   └── images/              # Profilbilder (z. B. Bewerbungsfoto)
├── dist/                    # Generierte PDF-Dateien (Lebensläufe & Anschreiben)
├── docs/                    # Nachweise, Zeugnisse & Zertifikate (lokal / privat, via .gitignore geschützt)
├── jobs/                    # Stellenbeschreibungen & Inserate (lokal / privat, via .gitignore geschützt)
├── skills/                  # Erweiterte Qualitätssicherungs- & Automatisierungs-Skills
│   ├── audit/               # Evidence- & Trust-Check gegen Zeugnisse
│   ├── fit/                 # Match-Score- & ATS-Analyse gegen Stelleninserat
│   ├── links/               # Link- & URL-Validierung
│   ├── make/                # PDF-Kompilierung & Vorschau
│   ├── spell/               # Rechtschreib- & Stilprüfung (Schweizer Orthografie)
│   └── test/                # Orchestrierte Gesamtprüfung aller Skills
├── src/                     # Quelldateien in Markdown
│   ├── cv-standard.md       # Standard-Lebenslauf
│   ├── cv-<firma>.md        # Unternehmensspezifischer Lebenslauf
│   └── letter-<firma>.md    # Unternehmensspezifisches Motivationsschreiben
├── templates/
│   ├── cv-template.tex      # LaTeX-Vorlage für Lebensläufe
│   └── letter-template.tex  # LaTeX-Vorlage für Motivationsschreiben
├── .gitignore               # Ausschluss sensibler Dokumente & temporärer Dateien
├── Makefile                 # Make-Automatisierung für Build & Vorschau
├── opencode.json            # Konfiguration für lokale Skills und Assistenten
└── README.md                # Projektdokumentation
```

---

## Voraussetzungen & Installation

Auf macOS werden [Homebrew](https://brew.sh), Pandoc und eine LaTeX-Distribution (BasicTeX oder MacTeX) benötigt.

### 1. Basispakete via Homebrew installieren
```bash
brew install pandoc
brew install --cask basictex
```

*Alternativ kann die vollständige MacTeX-Distribution installiert werden:*
```bash
brew install --cask mactex
```

### 2. LaTeX-Pakete aktualisieren und nachinstallieren
Nach der Installation von BasicTeX muss das Terminal gegebenenfalls neu gestartet werden. Anschliessend werden die zusätzlich benötigten LaTeX-Pakete installiert:

```bash
sudo tlmgr update --self
sudo tlmgr install moderncv fontawesome5
```

> **Hinweis:** Falls `xelatex` oder `tlmgr` nach der Installation nicht gefunden wird, das Terminal neu starten. Bei BasicTeX liegen die Programme üblicherweise unter `/Library/TeX/texbin`.

---

## Dokumente erstellen & kompilieren

### Schnelleinstieg mit `make`

```bash
# Alle vorhandenen Dokumente kompilieren
make all

# Dokumente für ein bestimmtes Ziel / Unternehmen bauen
make <firma>

# Nur Lebenslauf oder nur Anschreiben bauen
make cv-<firma>
make letter-<firma>

# Standard-Lebenslauf bauen
make standard
```

### Manuelle Kompilierung via Pandoc

```bash
# Lebenslauf kompilieren
pandoc src/cv-<firma>.md \
  --template=templates/cv-template.tex \
  --pdf-engine=xelatex \
  --shift-heading-level-by=-1 \
  -o dist/cv-<firma>.pdf

# Motivationsschreiben kompilieren
pandoc src/letter-<firma>.md \
  --template=templates/letter-template.tex \
  --pdf-engine=xelatex \
  -o dist/letter-<firma>.pdf
```

---

## Qualitätssicherungs-Skills

Das Projekt beinhaltet spezialisierte Skills zur automatisierten Prüfung und Optimierung von Bewerbungsunterlagen:

| Skill | Zweck & Funktion |
| :--- | :--- |
| **`make`** | Kompiliert Lebensläufe und Motivationsschreiben mit Pandoc/XeLaTeX und öffnet das PDF direkt in der macOS-Vorschau. |
| **`spell`** | Prüft Rechtschreibung, Grammatik, Zeichensetzung, IT-Komposita und Schweizer Rechtschreibregeln (konsequent *ss* statt *ß*). |
| **`fit`** | Analysiert den Match-Score (0–100%) zwischen Stelleninserat (`jobs/<firma>.md`) und Lebenslauf (`src/cv-<firma>.md`), inklusive ATS-Keyword-Prüfung und Lückenanalyse. |
| **`audit`** | Führt einen Trust- & Evidence-Check anhand der Nachweise in `docs/` durch (Prüfung von Daten, Noten, Diplomen und Zeugnissen). |
| **`links`** | Überprüft alle URLs, Hyperlinks und E-Mail-Adressen in den Markdown-Dateien und generierten PDFs auf Erreichbarkeit (HTTP 200). |
| **`test`** | Orchestriert eine ganzheitliche Qualitätsprüfung (`fit`, `audit`, `spell`, `links`) und fasst das Ergebnis in einer kompakten Status-Ampel zusammen. |

---

## Workflow: Neues Bewerbungsdossier anlegen

1. **Stelleninserat hinterlegen:** Anforderungsprofil unter `jobs/<firma>.md` ablegen.
2. **Dokumente erstellen:** Neue Markdown-Dateien unter `src/cv-<firma>.md` und `src/letter-<firma>.md` anlegen (z. B. auf Basis von `src/cv-standard.md`).
3. **Qualität prüfen:** 
   - Rechtschreibung prüfen mit Skill `spell`
   - Passgenauigkeit prüfen mit Skill `fit`
   - Nachweise abgleichen mit Skill `audit`
4. **PDFs generieren:** `make <firma>` ausführen. Die Dokumente werden in `dist/` abgelegt und zur Prüfung geöffnet.

---

## Sicherheit & Datenschutz

Da Bewerbungsunterlagen, Arbeitszeugnisse und Zertifikate vertrauliche personenbezogene Daten enthalten:
- Sind die Ordner `docs/` und `jobs/` sowie die generierten PDFs (`dist/`) in `.gitignore` eingetragen.
- Sollte das Repository stets privat betrieben werden.
