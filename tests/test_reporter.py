
from io import StringIO

import pytest
from rich.console import Console

from repoready import reporter


@pytest.mark.parametrize(
    ("test_status", "expected_output"),
    [
        ("Found", "FOUND"),
        ("Empty", "EMPTY"),
        ("Missing", "MISSING"),
    ],
)
def test_terminal_report_displays_correct_test_status(
    monkeypatch, test_status, expected_output
):
    """Check that terminal reports display all test directory states."""

    output = StringIO()

    test_exists = test_status != "Missing"

    scan_results = {
        "tests/": {
            "description": "Automated Python test directory",
            "exists": test_exists,
            "has_test_files": test_status == "Found",
            "test_file_count": 1 if test_status == "Found" else 0,
            "status": test_status,
        }
    }

    health = {
        "score": 80,
        "grade": "Good",
        "found": 5,
        "missing": 1,
    }

    test_console = Console(file=output, force_terminal=False)
    monkeypatch.setattr(reporter, "console", test_console)

    reporter.display_report(scan_results, health)

    report = output.getvalue()

    assert expected_output in report


def test_terminal_report_preserves_required_file_status(monkeypatch):
    """Check that other required files retain their existing behavior."""

    output = StringIO()

    scan_results = {
        "README.md": {
            "description": "Project documentation",
            "exists": True,
            "status": "Found",
        },
        "LICENSE": {
            "description": "Open-source license",
            "exists": False,
            "status": "Missing",
        },
    }

    health = {
        "score": 50,
        "grade": "Poor",
        "found": 1,
        "missing": 1,
    }

    test_console = Console(file=output, force_terminal=False)
    monkeypatch.setattr(reporter, "console", test_console)

    reporter.display_report(scan_results, health)

    report = output.getvalue()

    assert "FOUND" in report
    assert "MISSING" in report
