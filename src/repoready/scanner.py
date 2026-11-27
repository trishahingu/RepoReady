
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
    Scan a local repository for essential open-source files.
    """

    root = Path(repo_path).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Repository not found: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    results = {}

    for filename, description in REQUIRED_FILES.items():
        file_path = root / filename

        results[filename] = {
            "description": description,
            "exists": file_path.is_file(),
            "status": "Found" if file_path.is_file() else "Missing",
        }

    tests_path = root / "tests"

    results["tests/"] = {
        "description": "Automated test directory",
        "exists": tests_path.is_dir(),
        "status": "Found" if tests_path.is_dir() else "Missing",
    }

    return results
