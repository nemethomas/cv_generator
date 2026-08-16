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

.PHONY: all clean example cv-example letter-example dossier sync scout links help

# Standard: alle vorhandenen Dokumente bauen
all: $(PDFS)

# Hilfe & Befehlsübersicht
help:
	@echo "📋 Verfügbare Make-Befehle:"
	@echo "  make <firma>        Kompiliert Lebenslauf & Anschreiben für <firma> (z. B. make zkb)"
	@echo "  make cv-<firma>     Kompiliert nur den Lebenslauf (z. B. make cv-zkb)"
	@echo "  make letter-<firma> Kompiliert nur das Anschreiben (z. B. make letter-zkb)"
	@echo "  make all            Kompiliert alle vorhandenen Dokumente in src/"
	@echo "  make example        Baut die Standard-Beispieldokumente"
	@echo "  make dossier        Liest Nachweise in docs/ ein (OCR & dynamisches Profil)"
	@echo "  make scout          Startet die Stellensuche im Grossraum Zürich"
	@echo "  make links          Prüft Hyperlinks und URLs in Markdown und PDFs"
	@echo "  make clean          Löscht alle generierten PDFs im Ordner dist/"

# Stellensuche im Terminal
scout:
	@python3 skills/scout/search_jobs.py

# Link-Validierung
links:
	@python3 skills/links/check_links.py

# Dossier-Synchronisation (OCR & Aggregation aller Nachweise in docs/dossier.md & profile.json)
dossier sync:
	@python3 scripts/sync_dossier.py

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

# Dynamische Kurz-Targets für beliebige Ziele (z. B. make cv-<name>, make letter-<name>, make <name>)
cv-%: $(DIST_DIR)/cv-%.pdf ;
letter-%: $(DIST_DIR)/letter-%.pdf ;

%:
	@found=0; \
	if [ -f "$(SRC_DIR)/cv-$@.md" ]; then \
		$(MAKE) --no-print-directory $(DIST_DIR)/cv-$@.pdf; \
		found=1; \
	fi; \
	if [ -f "$(SRC_DIR)/letter-$@.md" ]; then \
		$(MAKE) --no-print-directory $(DIST_DIR)/letter-$@.pdf; \
		found=1; \
	fi; \
	if [ $$found -eq 0 ]; then \
		echo "❌ Keine Vorlage 'src/cv-$@.md' oder 'src/letter-$@.md' gefunden."; \
		echo "💡 Tipp: Lege die Datei an mit 'cp src/cv-example.md src/cv-$@.md' oder führe 'make help' aus."; \
		exit 1; \
	fi

clean:
	rm -rf $(DIST_DIR)/*.pdf
