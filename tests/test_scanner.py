
import json

import pytest

from repoready.cli import main
from repoready.scorer import calculate_health_score
from repoready.scanner import scan_repository


# --------------------------------
# Repository Scanner Tests
# --------------------------------

def test_scan_repository_finds_existing_files(tmp_path):
    """Check that the scanner identifies existing files."""

    (tmp_path / "README.md").write_text("# Test Project")
    (tmp_path / "LICENSE").write_text("MIT License")
    (tmp_path / "tests").mkdir()

    results = scan_repository(str(tmp_path))

    assert results["README.md"]["exists"] is True
    assert results["LICENSE"]["exists"] is True
    assert results["tests/"]["exists"] is True
    assert results["tests/"]["status"] == "Empty"


def test_scan_repository_detects_missing_files(tmp_path):
    """Check that missing files are reported correctly."""

    results = scan_repository(str(tmp_path))

    assert results["README.md"]["exists"] is False
    assert results["CONTRIBUTING.md"]["status"] == "Missing"
    assert results["tests/"]["status"] == "Missing"


def test_scan_repository_rejects_invalid_path():
    """Check that invalid repository paths raise an error."""

    with pytest.raises(FileNotFoundError):
        scan_repository("nonexistent_repository_12345")


def test_scan_repository_rejects_file_path(tmp_path):
    """Check that a file cannot be scanned as a directory."""

    file_path = tmp_path / "example.txt"
    file_path.write_text("Not a repository")

    with pytest.raises(NotADirectoryError):
        scan_repository(str(file_path))


def test_scan_repository_detects_test_files(tmp_path):
    """Check that Python test files are detected."""

    tests_path = tmp_path / "tests"
    tests_path.mkdir()

    (tests_path / "test_scanner.py").write_text(
        "def test_example():\n    assert True\n"
    )

    results = scan_repository(str(tmp_path))

    assert results["tests/"]["exists"] is True
    assert results["tests/"]["has_test_files"] is True
    assert results["tests/"]["test_file_count"] == 1
    assert results["tests/"]["status"] == "Found"


def test_scan_repository_detects_empty_tests_directory(tmp_path):
    """Check that an empty tests directory is identified."""

    (tmp_path / "tests").mkdir()

    results = scan_repository(str(tmp_path))

    assert results["tests/"]["exists"] is True
    assert results["tests/"]["has_test_files"] is False
    assert results["tests/"]["test_file_count"] == 0
    assert results["tests/"]["status"] == "Empty"


def test_scan_repository_detects_nested_test_files(tmp_path):
    """Check that test files in nested directories are detected."""

    nested_tests = tmp_path / "tests" / "unit"
    nested_tests.mkdir(parents=True)

    (nested_tests / "test_example.py").write_text(
        "def test_example():\n    assert True\n"
    )

    results = scan_repository(str(tmp_path))

    assert results["tests/"]["has_test_files"] is True
    assert results["tests/"]["test_file_count"] == 1
    assert results["tests/"]["status"] == "Found"


def test_scan_repository_detects_alternative_test_filename(tmp_path):
    """Check that files ending with _test.py are detected."""

    tests_path = tmp_path / "tests"
    tests_path.mkdir()

    (tests_path / "scanner_test.py").write_text(
        "def test_example():\n    assert True\n"
    )

    results = scan_repository(str(tmp_path))

    assert results["tests/"]["has_test_files"] is True
    assert results["tests/"]["status"] == "Found"


# --------------------------------
# Health Score Tests
# --------------------------------

def test_health_score_all_files_found():
    results = {
        "README.md": {"exists": True},
        "LICENSE": {"exists": True},
        "tests/": {"exists": True},
    }

    score = calculate_health_score(results)

    assert score["score"] == 100
    assert score["grade"] == "Excellent"


def test_health_score_missing_files():
    results = {
        "README.md": {"exists": True},
        "LICENSE": {"exists": False},
        "tests/": {"exists": False},
    }

    score = calculate_health_score(results)

    assert score["score"] == 33
    assert score["grade"] == "Poor"
    assert score["missing"] == 2


def test_health_score_empty_results():
    score = calculate_health_score({})

    assert score["score"] == 0
    assert score["grade"] == "N/A"


# --------------------------------
# CLI Tests
# --------------------------------

def test_cli_json_export(tmp_path, monkeypatch):
    """Check that CLI exports a JSON report."""

    (tmp_path / "README.md").write_text("# Test")
    output = tmp_path / "report.json"

    monkeypatch.setattr(
        "sys.argv",
        ["repoready", str(tmp_path), "--json", str(output)]
    )

    main()

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["health"]["score"] >= 0
    assert "README.md" in data["files"]


def test_cli_markdown_export(tmp_path, monkeypatch):
    """Check that CLI exports a Markdown report."""

    (tmp_path / "README.md").write_text("# Test")
    output = tmp_path / "report.md"

    monkeypatch.setattr(
        "sys.argv",
        ["repoready", str(tmp_path), "--markdown", str(output)]
    )

    main()

    assert output.exists()

    content = output.read_text(encoding="utf-8")

    assert "# RepoReady - Repository Health Report" in content
    assert "README.md" in content


def test_cli_invalid_repository_path(monkeypatch):
    """Check that CLI handles invalid repository paths."""

    monkeypatch.setattr(
        "sys.argv",
        ["repoready", "nonexistent_repository_12345"]
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 1


def test_cli_json_export_invalid_path(tmp_path, monkeypatch):
    """Check that CLI handles invalid JSON export paths."""

    output = tmp_path / "missing_folder" / "report.json"

    monkeypatch.setattr(
        "sys.argv",
        ["repoready", str(tmp_path), "--json", str(output)]
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 1
    assert not output.exists()
