import os
import shutil
from pathlib import Path
import allure
import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def clean_allure_results():
    results_dir = Path("reports/allure-results")
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    yield


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.muji.com.vn/vn")


@pytest.fixture(scope="session")
def http_session():
    s = requests.Session()
    yield s
    s.close()


@pytest.fixture(autouse=True)
def capture_playwright_artifacts(request, page, context):
    trace_dir = Path("reports/traces")
    trace_dir.mkdir(parents=True, exist_ok=True)

    safe_name = request.node.nodeid.replace(os.sep, "_").replace(":", "_").replace("/", "_")
    request.node._trace_path = trace_dir / f"{safe_name}.zip"

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = item.funcargs.get("page")
        context = item.funcargs.get("context")
        trace_path = getattr(item, "_trace_path", None)

        if context is not None and trace_path is not None:
            try:
                context.tracing.stop(path=str(trace_path))
            except Exception:
                pass

        if report.failed and page is not None and trace_path is not None:
            screenshot_path = trace_path.with_suffix(".png")
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(
                    str(screenshot_path),
                    name=f"{item.name}_failure.png",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                allure.attach(
                    f"Screenshot capture failed: {exc}",
                    name="screenshot_error",
                    attachment_type=allure.attachment_type.TEXT,
                )

            try:
                allure.attach.file(
                    str(trace_path),
                    name=f"{item.name}_trace.zip",
                    attachment_type=allure.attachment_type.ZIP,
                )
            except Exception as exc:
                allure.attach(
                    f"Trace capture failed: {exc}",
                    name="trace_error",
                    attachment_type=allure.attachment_type.TEXT,
                )

