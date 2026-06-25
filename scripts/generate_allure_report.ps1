param(
    [string]$ResultsDir = "reports/allure-results",
    [string]$ReportDir = "reports/allure-report"
)

if (-not (Test-Path $ResultsDir)) {
    Write-Error "Allure results directory '$ResultsDir' not found. Run pytest first to generate results (pytest --alluredir=$ResultsDir)"
    exit 1
}

Write-Output "Generating Allure report from $ResultsDir -> $ReportDir"
allure generate $ResultsDir -o $ReportDir --clean
if ($LASTEXITCODE -ne 0) { Write-Error "allure generate failed (exit $LASTEXITCODE)"; exit $LASTEXITCODE }

Write-Output "Opening Allure report..."
allure open $ReportDir
