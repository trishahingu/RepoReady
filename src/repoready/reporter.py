
import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def display_report(scan_results: dict, health: dict):
    """Display repository scan results in the terminal."""

    console.print(
        Panel(
            "[bold cyan]RepoReady[/bold cyan]\n"
            "Open Source Repository Health Checker",
            border_style="cyan",
        )
    )

    table = Table(title="Repository Analysis")

    table.add_column("File", style="cyan")
    table.add_column("Description")
    table.add_column("Status", justify="center")

    for filename, details in scan_results.items():
        if filename == "tests/":
            test_status = details["status"].lower()

            if test_status == "found":
                status = "[green]FOUND[/green]"
            elif test_status == "empty":
                status = "[yellow]EMPTY[/yellow]"
            else:
                status = "[red]MISSING[/red]"
        else:
            status = (
                "[green]FOUND[/green]"
                if details["exists"]
                else "[red]MISSING[/red]"
            )

        table.add_row(
            filename,
            details["description"],
            status,
        )

    console.print(table)

    score = health["score"]

    console.print(
        Panel(
            f"[bold green]Health Score: {score}/100[/bold green]\n"
            f"Grade: {health['grade']}\n"
            f"Found: {health['found']}\n"
            f"Missing: {health['missing']}",
            title="Repository Health",
            border_style="green",
        )
    )


def export_json_report(scan_results: dict, health: dict, output_path: str):
    """Export repository analysis as JSON."""

    report = {
        "project": "RepoReady",
        "generated_at": datetime.now().astimezone().isoformat(),
        "health": health,
        "files": scan_results,
    }

    Path(output_path).write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )


def export_markdown_report(scan_results: dict, health: dict, output_path: str):
    """Export repository analysis as Markdown."""

    lines = [
        "# RepoReady - Repository Health Report",
        "",
        f"**Health Score:** {health['score']}/100",
        f"**Grade:** {health['grade']}",
        f"**Found:** {health['found']}",
        f"**Missing:** {health['missing']}",
        "",
        "## File Analysis",
        "",
        "| File | Description | Status |",
        "|---|---|---|",
    ]

    for filename, details in scan_results.items():
        status = "Found" if details["exists"] else "Missing"

        lines.append(
            f"| {filename} | {details['description']} | {status} |"
        )

    Path(output_path).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
