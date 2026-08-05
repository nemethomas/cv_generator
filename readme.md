Template (z. B. moderncv-Klasse) definiert Layout, Foto-Position, Farben, Schrift
Pandoc liest deine lebenslauf.md und "füllt" das LaTeX-Template mit den Inhalten
xelatex/pdflatex compiliert das Ganze zu einem PDF


lebenslauf.md  →  (Pandoc + Template)  →  lebenslauf.tex  →  (xelatex)  →  lebenslauf.pdf

brew install pandoc
brew install --cask basictex   # oder mactex für alles

# Nur einmalig – fehlende Pakete für moderncv nachinstallieren:
sudo tlmgr install moderncv fontawesome5

# Export:

cd zu ordner

  pandoc Thomas_Nemeth_CV.md \
  --template=cv-template.tex \
  --pdf-engine=xelatex \
  --shift-heading-level-by=-1 \
  -o Thomas_Nemeth_CV.pdf

  
