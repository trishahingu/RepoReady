
import argparse
import sys

from repoready.scanner import scan_repository
from repoready.scorer import calculate_health_score
from repoready.reporter import (
    display_report,
    export_json_report,
    export_markdown_report,
)


def main():
    parser = argparse.ArgumentParser(
        prog="repoready",
        description="Analyze a repository's open-source health."
    )
    parser.add_argument(
    "--version",
    action="version",
    version="RepoReady 0.1.0",
)
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the repository"
    )

    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Export report as JSON"
    )

    parser.add_argument(
        "--markdown",
        metavar="FILE",
        help="Export report as Markdown"
    )

    args = parser.parse_args()

    try:
        results = scan_repository(args.path)
        health = calculate_health_score(results)

        display_report(results, health)

        if args.json:
            export_json_report(results, health, args.json)
            print(f"JSON report saved to: {args.json}")

        if args.markdown:
            export_markdown_report(results, health, args.markdown)
            print(f"Markdown report saved to: {args.markdown}")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
