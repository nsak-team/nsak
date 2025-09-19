.PHONY: dev
dev:
	python -m http.server -d app || python3 -m http.server -d app


./docs/documentation/documentation.pdf: ./docs/documentation/documentation.tex
	cd ./docs/documentation \
	&& latexmk -pdflua


.PHONY: docs
docs: ./docs/documentation/documentation.pdf


.PHONY: clean-docs
clean-docs:
	cd ./docs/documentation \
	&& latexmk -c