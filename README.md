# Swiss Army Knife Network Sniffer
@TODO: Add abstract

## About
This repository contains all relevant documentation,
configuration and code for the BFH (Bern University of Applied Sciences) Module "BTI3041 - Project 2".

### Authors
- Frank Gauss <gausf1@bfh.ch>
- Lukas von Allmen <vonal3@bfh.ch>

### Stakeholders
- Wenger Hansjürg <wgh1@bfh.ch>
- Urs Keller <>
TODO: Ask expert and tutor if we are allowed to them to the readme

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
make <thesis|project2> <documentation|presentation>

# For example the following command renders the thesis documentation as PDF
make thesis documentaiton
```

### Clean documentation, including the generated PDF
```bash
make clean <thesis|project2> <documentation|presentation>
```

## Installation

To build and install the nsak executable, run the following commands:

```bash
# Build and install nsak executable
uv build
# uv tool install dist/nsak-<version>-py3-none-any.whl
uv tool install dist/nsak-0.1.0-py3-none-any.whl
```

## Usage

NSAK CLI
```bash
# List all subcommands for the nsak CLI
nsak -help
```

### Simulate a specific scenario in a environment

**Host system configuration:**
```
# Install iproute2 if not already installed
sudo apt install iproute2

# Create a dummy interface called `nsak0` for simulation:
sudo ip link add nsak0 type dummy
sudo ip link set nsak0 up

# Verify that the interface was created successfully and is in state UP or UNKNOWN:
ip link show nsak0
```

**Simulate the scenario `mitm` in the environment `simple_tcp_client_server`:
```bash
nsak environment list # Shows all available environments
nsak environment list_scenarios simple_tcp_client_server # Lists all available scenarios for the environment
nsak scenario build mitm # Build the scenario which you want to simulate
nsak environment simulate simple_tcp_client_server mitm
```

## Development

@TODO: Describe development environment

### Programming Language

nsak and all scenarios and drills are written in Python.

### Virtual Environment and Package Management

The virtual environment and packages are management with [uv](https://docs.astral.sh/uv/). The required python version and all dependencies are configured in `pyproject.toml`. To create a virtual environment and install all dependencies, run the following command:

`uv sync`

### Install nsak module in editable mode

For development and the build process to work correctly, it is required to install nsak in editable mode with the following command:

`uv pip install -e .`

### Enable nsak command completion

Command works only when running `nsak` over an entrypoint e.g., after installing it with `uv tool install nsak`.

**Bash**
```bash
echo "_NSAK_COMPLETE=bash_source nsak" >> ~/.bashrc
```

**Zsh**
```bash
echo "_NSAK_COMPLETE=zsh_source nsak" >> ~/.zshrc
```

**Fish**
```bash
echo "_NSAK_COMPLETE=fish_source nsak" > ~/.config/fish/completions/nsak.fish
```

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
