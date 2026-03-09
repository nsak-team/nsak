DOCUMENTATION_PATH = docs

PROJECTS := project2 thesis
FORMATS  := documentation presentation

$(PROJECTS):
	$(eval PROJECT := $@)

$(FORMATS):
	@if [ -z "$(PROJECT)" ]; then \
		echo "Choose project first"; exit 1; \
	fi
	$(MAKE) build PROJECT=$(PROJECT) TYPE=$@

build:
	cd docs/$(PROJECT)/$(TYPE) && \
	latexmk -pdflua --shell-escape

clean:
	rm -rf docs/$(PROJECT)/$(TYPE)/$(TYPE).pdf
