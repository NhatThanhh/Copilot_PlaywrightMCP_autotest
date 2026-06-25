# Python + pytest automation framework

This project contains a minimal automation testing framework using Python and `pytest`.

Quick start

1. Create a virtual environment and activate it.

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) If using Playwright browser tests, install browsers:
```powershell
python -m playwright install
```

3. Run tests:
```powershell
python -m pytest -q
```

Allure Report
1. Install Allure CLI (required to generate HTML report).
	- Windows (chocolatey): `choco install allure.commandline -y`
	- Windows (scoop): `scoop install allure`
	- macOS (brew): `brew install allure`
	- Linux: follow https://docs.qameta.io/allure/

2. Run pytest to collect results (Allure results folder is configured):
```powershell
python -m pytest --alluredir=reports/allure-results
```

3. Generate and open the report:
```powershell
.\scripts\generate_allure_report.ps1
```

Or on bash/mac:
```bash
./scripts/generate_allure_report.sh
```

Files added
- `requirements.txt` — deps
- `pytest.ini` — pytest config
- `tests/conftest.py` — common fixtures
- `tests/test_sample.py` — example tests
- `tests/pages/home_page.py` — simple page object
- `scripts/run_tests.ps1`/`run_tests.sh` — convenience runners
