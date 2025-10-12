# Swiss Army Knife Network Sniffer
@TODO: Add abstract

## About
This repository contains all relevant documentation, 
configuration and code for the BFH (Bern University of Applied Sciences) Module "BTI3041 - Project 2".

### Authors
- Frank Gauss <gausf1@bfh.ch>
- Lukas von Allmen <vonal3@bfh.ch>

### Tutor
- Wenger Hansjürg <wgh1@bfh.ch>

## Documentation
The project documentation is written in LaTeX and can be found in the `docs/` folder.

To build the documentation, you need to install LaTeX on your system, which may take several hours to complete:
- LaTeX quick installation guide: https://tug.org/texlive/quickinstall.html
- LaTeX full installation guide: https://tug.org/texlive/doc/texlive-en/texlive-en.html#installation

Check the following links for the BFH LaTeX templates, which are used for the documentation:
- Installation: https://latex.ti.bfh.ch/doc_gettingStarted/index.html
- BFH Thesis Class: https://latex.ti.bfh.ch/doc_bfhclass/thesis.html

### Build PDF documentation
```bash
make docs
```

### Clean documentation, including the generated PDF
```bash
make clean-docs
```

### Clean and rebuild PDF documentation
```bash
make clean-docs && make docs
```

## License
@TODO: Evaluate and add license

### timeline
```mermaid
gantt
    title Project 2 Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1: Planning
    Kickoff :a1, 2025-09-12, 14d
    Kickoff :a2, 2025-09-26, 14d
    Concept Phase :a3, 2025-10-10, 14d
    Design & Timeplan :a4, 2025-10-24, 14d
    POC :aa5, 2025-11-28, 28
