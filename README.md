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

## Development

@TODO: Describe development environment

### Programming Language

nsak and all scenarios and drills are written in Python.

### Virtual Environment and Package Management

The virtual environment and packages are management with [uv](https://docs.astral.sh/uv/). The required python version and all dependencies are configured in `pyproject.toml`. To create a virtual environment and install all dependencies, run the following command:

`uv init`

### Linting and Formatting

Linting and formatting is done using [ruff](https://docs.astral.sh/ruff/). The configuration is located in `pyproject.toml`. To run linting and formatting, run the following command:

`uvx ruff check`

### Type Checking

Type checking is done using [mypy](https://www.mypy-lang.org/). The configuration is located in `pyproject.toml`. To run type checking, run the following command:

`uvx mypy`

### GIT Pre-Commit Hooks

GIT pre-commit hooks are set up with [pre-commit](https://pre-commit.com/) to enforce linting, formatting and type checking on every commit. The configuration is located in `.pre-commit-config.yaml`. It's strongly recommended to install pre-commit hooks locally before committing any changes:

`uvx pre-commit install`

Additional links:
 - ruff pre-commit: https://github.com/astral-sh/ruff-pre-commit
 - mypy pre-commit: https://github.com/pre-commit/mirrors-mypy

## License
@TODO: Evaluate and add license

### timeline

```mermaid
timeline
    title Project 2 Timeline
    section Planning & Brainstorm
    🗓️ 2025-09-12 : Kickoff & Setup
    🗓️ 2025-09-26 : Planning
    🗓️ 2025-10-10 : Research & Analysis
    section Design & Resarch
    🗓️ 2025-10-24 : Concept & Timeplan
    2025-11-02 : Research & Product comparison
    🗓️ 2025-11-07 : Architecture and Design
    section Implementation
    🗓️ 2025-11-21 : Finalized Scenario MITM with required drills and environments 
    🗓️ 2025-12-05 : Finalized Scenario "W-lan Spoofing" with required drills and enviornments
    🗓️ 2025-12-19 : Integration & Testing 
    section Documentation & Delivery
    2025-01-03 : Final Presentation and Documentation finish
    2025-01-16 : Final Presentation 
    2025-01-19 : Project Submission 
 ```
### changed timeline

```mermaid
timeline
    title Project 2 Timeline
    section Planning & Brainstorm
    🗓️ 2025-09-12 : Kickoff & Setup
    🗓️ 2025-09-26 : Planning
    🗓️ 2025-10-10 : Research & Analysis
    section Design & Resarch
    🗓️ 2025-10-24 : Concept & Timeplan
    2025-11-02 : Research & Product comparison
    🗓️ 2025-11-07 : Architecture and Design
    section Hardware Setup
    🗓️ 2025-11-28 : Nano Pi r76s, Banana Pi R4 with debian image and configured interfaces
    section Implementation
    2025-12-05 : POC nsak framework 
    🗓️ 2025-12-19 : Finalized Scenario MITM with required drills and environments, integration and testing
    🗓️ 2025-12-19 : Finalized Scenario "W-lan Spoofing" with required drills and enviornments, integration and testing
    section Documentation & Delivery
    2025-01-03 : Final Presentation and Documentation finish
    2025-01-16 : Final Presentation 
    2025-01-19 : Project Submission 
```
