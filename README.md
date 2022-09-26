# SudoQGen
A Sudoku image generator


## Setup

create a virtual env:
```bash
virtualenv --python C:\Path\To\Python\python.exe venv
```

Activate the environment:
* Windows
```bash
.\venv\Scripts\activate
```

* Linux
```bash
source venv/bin/activate
```

isntall the requirements:
```bash
pip install -e .[dev]
```

## Examples
run a simple example generating images using:
```bash
python -m "sudoqgen.main"
```