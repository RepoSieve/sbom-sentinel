# Run The Current Skeleton

The current project is a skeleton. It proves that the package structure,
CLI entry point, test setup, and demo script are ready for feature work.

It does not yet parse SBOM files, query OSV, or rank vulnerabilities.

## 1. Clone the repository

```bash
git clone https://github.com/RepoSieve/sbom-sentinel.git
cd sbom-sentinel
```

If already cloned:

```bash
git checkout main
git pull origin main
```

## 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install locally

```bash
python -m pip install -e .
```

If needed:

```bash
python3 -m pip install -e .
```

## 4. Run CLI help

```bash
python -m sbom_sentinel --help
```

Expected:

```text
usage: sbom_sentinel [-h] [--version]
```

## 5. Run version check

```bash
python -m sbom_sentinel --version
```

Expected:

```text
0.1.0
```

## 6. Run smoke tests

macOS/Linux:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

Expected:

```text
Ran 1 test

OK
```

## 7. Run demo script

```bash
scripts/run_demo.sh
```

Expected behavior: the script prints the current CLI help text.

## Troubleshooting

If `python` does not work, try `python3`.

If imports fail, confirm the virtual environment is active and run:

```bash
python -m pip install -e .
```

If tests fail after pulling latest `main`, create a bugfix branch and open a PR with the failure details.
