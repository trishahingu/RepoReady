# 🚀 RepoReady

![RepoReady Tests](https://github.com/trishahingu/RepoReady/actions/workflows/tests.yml/badge.svg)

**Make your repository ready for contributors.**

RepoReady is an open-source Python tool that analyzes local repositories and checks whether essential files and structures are present for open-source collaboration. It provides both a command-line interface (CLI) and an interactive Streamlit dashboard.

## ✨ Features

- 📁 **Repository Scanner** – Checks essential project files and directories.
- 📊 **Health Score** – Calculates a repository health score out of 100.
- 🖥️ **CLI Interface** – Analyze repositories directly from your terminal.
- 🌐 **Interactive Dashboard** – Analyze repositories through a Streamlit web interface.
- 📄 **JSON Export** – Generate machine-readable analysis reports.
- 📝 **Markdown Export** – Generate readable repository reports.
- 💡 **Improvement Recommendations** – Identify missing files and suggested improvements.
- ⚡ **Version & Help** – Access CLI version and command information.

## 🛠️ Technologies

- Python
- Streamlit
- argparse
- Rich
- pytest

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/trishahingu/RepoReady.git
cd RepoReady
```

Install RepoReady with development and dashboard dependencies:

```bash
python -m pip install -e ".[dashboard,dev]"
```

## 🚀 Usage

### Command-Line Interface

Analyze the current repository:

```bash
repoready .
```

Analyze another repository:

```bash
repoready "path/to/repository"
```

Export a JSON report:

```bash
repoready . --json report.json
```

Export a Markdown report:

```bash
repoready . --markdown report.md
```

Display the version:

```bash
repoready --version
```

Display help:

```bash
repoready --help
```

### 🌐 Streamlit Dashboard

Launch the interactive dashboard:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

Enter your repository's local path and click **Analyze Repository**.

### Dashboard Features

- Repository path input and scanning.
- Visual repository health score.
- Files found and missing statistics.
- Repository analysis table.
- JSON and Markdown report downloads.
- Automatic improvement recommendations.
- About and usage guide pages.

## 🔍 What Does RepoReady Check?

| Check | Purpose |
|---|---|
| README.md | Project documentation |
| LICENSE | Open-source license |
| CONTRIBUTING.md | Contribution guidelines |
| CODE_OF_CONDUCT.md | Community standards |
| .gitignore | Git ignore configuration |
| pyproject.toml | Project configuration |
| tests/ | Automated test directory |

RepoReady calculates a basic readiness score based on the presence of these checks. It is an initial assessment, not a complete evaluation of repository quality.

## 🧪 Run Tests

Run the test suite:

```bash
python -m pytest tests/ -v
```

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Run the tests.
5. Submit a pull request.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 👩‍💻 Author

**Trisha Hingu**

GitHub: [@trishahingu](https://github.com/trishahingu)

---

⭐ If you find RepoReady useful, consider giving the repository a star!