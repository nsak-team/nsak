DOCUMENTATION_PATH = docs/documentation
DOCUMENTATION_FILE = documentation
DOCUMENTATION = $(DOCUMENTATION_PATH)/$(DOCUMENTATION_FILE)\

PRESENTATION_PATH = docs/presentation
PRESENTATION_FILE = nsak-presentation
PRESENTATION = $(PRESENTATION_PATH)/$(PRESENTATION_FILE)

.PHONY: docs clean-docs

docs: clean-docs $(DOCUMENTATION).pdf

$(DOCUMENTATION).pdf: $(DOCUMENTATION).tex
	cd $(DOCUMENTATION_PATH) && \
	latexmk -pdflua

clean-docs:
	rm -f $(DOCUMENTATION).pdf

presentation: clean-presentation $(PRESENTATION).pdf

$(PRESENTATION).pdf: $(PRESENTATION).tex
	cd $(PRESENTATION_PATH) && \
	latexmk -pdflua

clean-presentation:
	rm -f $(PRESENTATION).pdf
