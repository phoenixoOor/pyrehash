# pyrehash - Professional Hash Cracker

A modular, extensible security audit tool for password recovery and hash analysis.

## Features
- **Modular Architecture**: Easy to extend with new algorithms and attack types.
- **Advanced Attacks**: Dictionary, Brute-force, Hybrid, Rule-based, and Rainbow tables.
- **Performance**: Multi-processing and thread pool support for maximum speed.
- **Session Management**: Save and resume attacks with SQLite backend.
- **Modern CLI**: Built with `Typer` for a great user experience.
- **REST API**: Integrated FastAPI for remote control.

## Installation
```bash
pip install -e .
```

## Quick Start
```bash
# Dictionary attack
pyrehash crack -t 5f4dcc3b5aa765d61d8327deb882cf99 -m dict -f data/dictionaries/common.txt

# Brute-force attack
pyrehash crack -t 5f4dcc3b5aa765d61d8327deb882cf99 -m brute -l 6 -c lower
```

## Disclaimer
This tool is for legal security auditing and educational purposes only. Unauthorized access to computer systems is illegal.
