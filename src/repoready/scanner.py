
from pathlib import Path

REQUIRED_FILES = {
    "README.md": "Project documentation",
    "LICENSE": "Open-source license",
    "CONTRIBUTING.md": "Contribution guidelines",
    "CODE_OF_CONDUCT.md": "Community standards",
    ".gitignore": "Git ignore configuration",
    "pyproject.toml": "Project configuration",
}


def scan_repository(repo_path: str) -> dict:
    """
    Scan a local repository for essential open-source files
    and check whether the tests directory contains Python test files.
    """

    root = Path(repo_path).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Repository not found: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    results = {}

    # Check required project files
    for filename, description in REQUIRED_FILES.items():
        file_path = root / filename
        exists = file_path.is_file()

        results[filename] = {
            "description": description,
            "exists": exists,
            "status": "Found" if exists else "Missing",
        }

    # Check tests directory
    tests_path = root / "tests"
    tests_exists = tests_path.is_dir()

    # Detect Python test files, including nested directories
    if tests_exists:
        test_files = {
            *tests_path.rglob("test_*.py"),
            *tests_path.rglob("*_test.py"),
        }
    else:
        test_files = set()

    has_test_files = bool(test_files)

    # Determine test directory status
    if not tests_exists:
        test_status = "Missing"
    elif not has_test_files:
        test_status = "Empty"
    else:
        test_status = "Found"

    results["tests/"] = {
        "description": "Automated Python test directory",
        "exists": tests_exists,
        "has_test_files": has_test_files,
        "test_file_count": len(test_files),
        "status": test_status,
    }

    return results
