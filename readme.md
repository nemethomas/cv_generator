# CV als Markdown und PDF

Dieses Repository enthält meinen Lebenslauf in einem formatunabhängigen Aufbau. Der Inhalt wird in Markdown gepflegt, während Layout, Farben, Schrift und die Position des Fotos separat in einem LaTeX-Template definiert werden.

## Funktionsweise

```text
Thomas_Nemeth_CV.md
        ↓
Pandoc + cv-template.tex
        ↓
Thomas_Nemeth_CV.tex
        ↓
XeLaTeX
        ↓
Thomas_Nemeth_CV.pdf
```

- `Thomas_Nemeth_CV.md` enthält die Inhalte des Lebenslaufs.
- `cv-template.tex` definiert das visuelle Erscheinungsbild, beispielsweise Layout, Farben, Schrift und Foto-Position.
- Pandoc überträgt die Inhalte aus der Markdown-Datei in das LaTeX-Template.
- XeLaTeX kompiliert das Ergebnis als PDF.

Dadurch lassen sich Inhalt und Gestaltung unabhängig voneinander bearbeiten.

## Voraussetzungen

Auf macOS werden [Homebrew](https://brew.sh), Pandoc und eine LaTeX-Distribution benötigt.

```bash
brew install pandoc
brew install --cask basictex
```

Alternativ zu BasicTeX kann die vollständige MacTeX-Distribution installiert werden:

```bash
brew install --cask mactex
```

Nach der Installation von BasicTeX muss das Terminal gegebenenfalls neu gestartet werden. Anschliessend werden die zusätzlich benötigten LaTeX-Pakete einmalig installiert:

```bash
sudo tlmgr update --self
sudo tlmgr install moderncv fontawesome5
```

## PDF erstellen

Zuerst im Terminal in den Ordner dieses Repositorys wechseln:

```bash
cd /pfad/zum/cv-repository
```

Danach den Lebenslauf exportieren:

```bash
pandoc Thomas_Nemeth_CV.md \
  --template=cv-template.tex \
  --pdf-engine=xelatex \
  --shift-heading-level-by=-1 \
  -o Thomas_Nemeth_CV.pdf
```

Die fertige PDF-Datei wird als `Thomas_Nemeth_CV.pdf` im selben Ordner gespeichert.

## Inhalt oder Gestaltung ändern

- Inhaltliche Änderungen werden ausschliesslich in `Thomas_Nemeth_CV.md` vorgenommen.
- Gestalterische Änderungen werden in `cv-template.tex` vorgenommen.
- Nach jeder Änderung wird der Exportbefehl erneut ausgeführt.

## Hinweise

Falls `xelatex` oder `tlmgr` nach der Installation nicht gefunden wird, zuerst das Terminal neu starten. Bei BasicTeX liegen die Programme üblicherweise unter `/Library/TeX/texbin`.

Da ein Lebenslauf persönliche Daten enthält, sollte das Repository nicht öffentlich sein.
