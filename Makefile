DOCUMENTATION_PATH = docs/documentation
DOCUMENTATION_FILE = documentation
DOCUMENTATION = $(DOCUMENTATION_PATH)/$(DOCUMENTATION_FILE)\

PRESENTATION_PATH = docs/presentations
PRESENTATION_FILE = Nsak-presentation
PRESENTATION = $(PRESENTATION_PATH)/$(PRESENTATION_FILE)

.PHONY: docs clean-docs

docs: clean-docs $(DOCUMENTATION).pdf

$(DOCUMENTATION).pdf: $(DOCUMENTATION).tex
	cd $(DOCUMENTATION_PATH) && \
	latexmk -pdflua

clean-docs:
	rm -f $(DOCUMENTATION).pdf

presentations: clean-presentations $(PRESENTATION).pdf

$(PRESENTATION).pdf: $(PRESENTATION).tex
	cd $(PRESENTATION_PATH) && \
	latexmk -pdflua

clean-presentations:
	rm -f $(PRESENTATION).pdf
