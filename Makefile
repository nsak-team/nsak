.PHONY: dev
dev:
	python -m http.server -d app || python3 -m http.server -d app

./docs/documentation/documentation.pdf: ./docs/documentation/documentation.tex
	cd ./docs/documentation \
	&& pdflatex --shell-escape documentation.tex \
	&& bibtex documentation \
	&& pdflatex --shell-escape documentation.tex \
	&& pdflatex --shell-escape documentation.tex

.PHONY: docs
docs: ./docs/documentation/documentation.pdf

.PHONY: clean
clean:
	find ./doc -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bbl' -o -name '*.blg' -o -name '*.out' -o -name '*.pdf' -o -name '*.lof' -o -name '*.lot' -o -name '*.toc' -o -name '*.snm' -o -name '*.nav' \) -delete