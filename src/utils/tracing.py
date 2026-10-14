import re
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext


def start_tracing(context: BrowserContext):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def test_failed(request: pytest.FixtureRequest) -> bool:
    reports = [getattr(request.node, f"rep_{when}", None) for when in ("setup", "call")]
    return any(report is not None and report.failed for report in reports)


def trace_path(request: pytest.FixtureRequest) -> Path:
    test_name = re.sub(r"[^\w.-]+", "_", request.node.name).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = request.config.rootpath / "test-result" / "traces" / f"{test_name}_{timestamp}.zip"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# saves the trace only if the test failed; use chunk=True for a context shared between tests
def stop_tracing(context: BrowserContext, request: pytest.FixtureRequest, chunk: bool = False):
    path = trace_path(request) if test_failed(request) else None
    if chunk:
        context.tracing.stop_chunk(path=path)
    else:
        context.tracing.stop(path=path)
