# Makefile zur Kompilierung von Lebensläufen und Motivationsschreiben mit Pandoc und XeLaTeX

CV_TEMPLATE = templates/cv-template.tex
LETTER_TEMPLATE = templates/letter-template.tex
ENGINE = xelatex
DIST_DIR = dist
SRC_DIR = src

# Quelldateien nach Typ
CV_SRCS = $(wildcard $(SRC_DIR)/cv-*.md)
LETTER_SRCS = $(wildcard $(SRC_DIR)/letter-*.md)

# Zieldateien: dist/<doktyp>-<ziel>.pdf
CV_PDFS = $(patsubst $(SRC_DIR)/cv-%.md, $(DIST_DIR)/cv-%.pdf, $(CV_SRCS))
LETTER_PDFS = $(patsubst $(SRC_DIR)/letter-%.md, $(DIST_DIR)/letter-%.pdf, $(LETTER_SRCS))
PDFS = $(CV_PDFS) $(LETTER_PDFS)

.PHONY: all clean example cv-example letter-example

# Standard: alle vorhandenen Dokumente bauen
all: $(PDFS)

# Standard-Beispieldokumente
example: $(DIST_DIR)/cv-example.pdf $(DIST_DIR)/letter-example.pdf
cv-example: $(DIST_DIR)/cv-example.pdf
letter-example: $(DIST_DIR)/letter-example.pdf

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

# Dynamische Kurz-Targets für beliebige Ziele (z. B. make cv-<name>, make letter-<name>)
cv-%: $(DIST_DIR)/cv-%.pdf ;
letter-%: $(DIST_DIR)/letter-%.pdf ;

clean:
	rm -rf $(DIST_DIR)/*.pdf
