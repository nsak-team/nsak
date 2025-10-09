DOCUMENTATION_PATH = docs/documentation
DOCUMENTATION_FILE = documentation
DOCUMENTATION = $(DOCUMENTATION_PATH)/$(DOCUMENTATION_FILE)

.PHONY: docs clean-docs

docs: clean-docs $(DOCUMENTATION).pdf

$(DOCUMENTATION).pdf: $(DOCUMENTATION).tex
	cd $(DOCUMENTATION_PATH) && \
	latexmk -pdflua

clean-docs:
	rm -f $(DOCUMENTATION).pdf
