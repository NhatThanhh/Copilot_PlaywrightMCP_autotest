#!/usr/bin/env bash
RESULTS_DIR=${1:-reports/allure-results}
REPORT_DIR=${2:-reports/allure-report}

if [ ! -d "$RESULTS_DIR" ]; then
  echo "Allure results directory '$RESULTS_DIR' not found. Run pytest first to generate results (pytest --alluredir=$RESULTS_DIR)"
  exit 1
fi

echo "Generating Allure report from $RESULTS_DIR -> $REPORT_DIR"
allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean
if [ $? -ne 0 ]; then echo "allure generate failed"; exit 2; fi

echo "Opening Allure report..."
allure open "$REPORT_DIR"
