# Makefile zur Kompilierung von Lebensläufen und Motivationsschreiben mit Pandoc und XeLaTeX

CV_TEMPLATE = templates/cv-template.tex
LETTER_TEMPLATE = templates/letter-template.tex
ENGINE = xelatex
DIST_DIR = dist
SRC_DIR = src

# Quelldateien nach Typ
CV_SRCS = $(wildcard $(SRC_DIR)/cv-*.md)
LETTER_SRCS = $(wildcard $(SRC_DIR)/letter-*.md)

# Zieldateien: dist/<doktyp>-<firma>.pdf
CV_PDFS = $(patsubst $(SRC_DIR)/cv-%.md, $(DIST_DIR)/cv-%.pdf, $(CV_SRCS))
LETTER_PDFS = $(patsubst $(SRC_DIR)/letter-%.md, $(DIST_DIR)/letter-%.pdf, $(LETTER_SRCS))
PDFS = $(CV_PDFS) $(LETTER_PDFS)

.PHONY: all clean help example cv-example letter-example adcubum cv-adcubum letter-adcubum standard cv-standard yousty cv-yousty letter-yousty

# Standard: alle Dokumente (CVs und Briefe) bauen
all: $(PDFS)

# Sammeltargets (baut CV + Anschreiben)
example: $(DIST_DIR)/cv-example.pdf $(DIST_DIR)/letter-example.pdf
adcubum: $(DIST_DIR)/cv-adcubum.pdf $(DIST_DIR)/letter-adcubum.pdf
yousty: $(DIST_DIR)/cv-yousty.pdf $(DIST_DIR)/letter-yousty.pdf
standard: $(DIST_DIR)/cv-standard.pdf

# Einzeltargets
cv-example: $(DIST_DIR)/cv-example.pdf
letter-example: $(DIST_DIR)/letter-example.pdf
cv-adcubum: $(DIST_DIR)/cv-adcubum.pdf
letter-adcubum: $(DIST_DIR)/letter-adcubum.pdf
cv-yousty: $(DIST_DIR)/cv-yousty.pdf
letter-yousty: $(DIST_DIR)/letter-yousty.pdf
cv-standard: $(DIST_DIR)/cv-standard.pdf

# Pattern-Regel für Lebensläufe
$(DIST_DIR)/cv-%.pdf: $(SRC_DIR)/cv-%.md $(CV_TEMPLATE)
	@mkdir -p $(DIST_DIR)
	pandoc $< --template=$(CV_TEMPLATE) --pdf-engine=$(ENGINE) --shift-heading-level-by=-1 -o $@
	@echo "✓ Generiert: $@"

# Pattern-Regel für Motivationsschreiben
$(DIST_DIR)/letter-%.pdf: $(SRC_DIR)/letter-%.md $(LETTER_TEMPLATE)
	@mkdir -p $(DIST_DIR)
	pandoc $< --template=$(LETTER_TEMPLATE) --pdf-engine=$(ENGINE) -o $@
	@echo "✓ Generiert: $@"

clean:
	rm -rf $(DIST_DIR)/*.pdf
