# CHMTOOL.py
Chemistry Calculator for Ti-84
Creating a Python progam that can be ran on Terminal / Calculator that can run a python shell.
Went complety off tack and start to incorparte phonlogy tree generations into code, might organize might not dont know might not be a holein or like the golden gun.

working on a biology/Chemistry golden gun, general universal tool for university students to help with classes.

Goal is to allow for any type of variable probelm can be solved within the program.
// So far biology is big on phonolgy trees and data for the earth will categorize the data into a running environment.


## Run

Run the toolkit without animation support from this directory:

```sh
python3 EVOCHEM
```

## Modules

- `EVOCHEM`: menu and application entry point
- `chemistry.py`: element data, mole/mass, gas laws, pH, and thermochemistry
- `conversions.py`: unit conversions
- `equations.py`: chemical formula parsing and equation balancing
- `phylogeny.py`: aligned DNA distances and UPGMA tree generation
- `animation.py`: optional 3D phylogeny animation rendering

To render a phylogeny animation, use Python 3.13 or newer and install ManimGX in a local virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install manimgx
.venv/bin/python EVOCHEM
```

