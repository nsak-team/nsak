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
timeline
    title Project 2 Timeline
    section Planning & Brainstorm
    2025-09-12 : Kickoff & Setup
    2025-09-26 : Planning
    2025-10-10 : Research & Analysis
    section Design & Resarch
    2025-10-24 : Concept & Timeplan
    2025-10-02 : Research & Product comparison
    2025-11-07 : Architecture and Design
    section Implementation
    2025-11-21 : Core Development
    2025-12-24 : Integration & Testing 
    section Documentation & Delivery
    2025-01-03 : Final Presentation and Documentation finish
    2025-01-16 : Final Presentation 
    2025-01-22 : Project Submission 

