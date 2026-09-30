import argparse
import json
import logging
from typing import Optional

from .analytics import Analytics
from .logger_config import setup_logging
from .manager import ProblemManager
from .reporter import Reporter
from .scheduler import RevisionScheduler


logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="dsa-tracker",
        description=(
            "DSA Progress and Revision Analyzer"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # =========================================================
    # ADD COMMAND
    # =========================================================

    add_parser = subparsers.add_parser(
        "add",
        help="Add a new DSA problem",
    )

    add_parser.add_argument(
        "--title",
        required=True,
        help="Problem title",
    )

    add_parser.add_argument(
        "--topic",
        required=True,
        help="DSA topic",
    )

    add_parser.add_argument(
        "--difficulty",
        required=True,
        choices=["Easy", "Medium", "Hard"],
        help="Problem difficulty",
    )

    add_parser.add_argument(
        "--platform",
        default="LeetCode",
        help="Problem platform",
    )

    add_parser.add_argument(
        "--status",
        default="Solved",
        choices=[
            "Solved",
            "Attempted",
            "Unsolved",
        ],
        help="Problem status",
    )

    add_parser.add_argument(
        "--date-solved",
        help="Date solved in YYYY-MM-DD format",
    )

    # =========================================================
    # LIST COMMAND
    # =========================================================

    list_parser = subparsers.add_parser(
        "list",
        help="List tracked problems",
    )

    list_parser.add_argument(
        "--search",
        help="Search problem titles",
    )

    list_parser.add_argument(
        "--topic",
        help="Filter by topic",
    )

    list_parser.add_argument(
        "--difficulty",
        choices=["Easy", "Medium", "Hard"],
        help="Filter by difficulty",
    )

    list_parser.add_argument(
        "--status",
        choices=[
            "Solved",
            "Attempted",
            "Unsolved",
        ],
        help="Filter by status",
    )

    list_parser.add_argument(
        "--platform",
        help="Filter by platform",
    )

    # =========================================================
    # VIEW COMMAND
    # =========================================================

    view_parser = subparsers.add_parser(
        "view",
        help="View a specific problem",
    )

    view_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Problem ID",
    )

    # =========================================================
    # UPDATE COMMAND
    # =========================================================

    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing problem",
    )

    update_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Problem ID",
    )

    update_parser.add_argument(
        "--title",
        help="New problem title",
    )

    update_parser.add_argument(
        "--topic",
        help="New topic",
    )

    update_parser.add_argument(
        "--difficulty",
        choices=["Easy", "Medium", "Hard"],
        help="New difficulty",
    )

    update_parser.add_argument(
        "--platform",
        help="New platform",
    )

    update_parser.add_argument(
        "--status",
        choices=[
            "Solved",
            "Attempted",
            "Unsolved",
        ],
        help="New problem status",
    )

    update_parser.add_argument(
        "--date-solved",
        help="New solved date",
    )

    # =========================================================
    # DELETE COMMAND
    # =========================================================

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a problem",
    )

    delete_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Problem ID",
    )

    # =========================================================
    # STATS COMMAND
    # =========================================================

    subparsers.add_parser(
        "stats",
        help="Show progress analytics",
    )

    # =========================================================
    # DUE COMMAND
    # =========================================================

    due_parser = subparsers.add_parser(
        "due",
        help="Show problems due for revision",
    )

    due_parser.add_argument(
        "--date",
        help="Check revisions due on a specific date",
    )

    # =========================================================
    # UPCOMING COMMAND
    # =========================================================

    upcoming_parser = subparsers.add_parser(
        "upcoming",
        help="Show upcoming revisions",
    )

    upcoming_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of upcoming days",
    )

    # =========================================================
    # REVISE COMMAND
    # =========================================================

    revise_parser = subparsers.add_parser(
        "revise",
        help="Record a problem revision",
    )

    revise_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Problem ID",
    )

    revise_parser.add_argument(
        "--rating",
        required=True,
        choices=[
            "again",
            "hard",
            "good",
            "easy",
        ],
        help="Revision performance rating",
    )

    revise_parser.add_argument(
        "--date",
        help="Revision date in YYYY-MM-DD format",
    )

    # =========================================================
    # HISTORY COMMAND
    # =========================================================

    history_parser = subparsers.add_parser(
        "history",
        help="Show revision history",
    )

    history_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Problem ID",
    )

    # =========================================================
    # IMPORT COMMAND
    # =========================================================

    import_parser = subparsers.add_parser(
        "import",
        help="Import problems from a JSON file",
    )

    import_parser.add_argument(
        "--file",
        required=True,
        help="Path to JSON file",
    )

    # =========================================================
    # REPORT COMMAND
    # =========================================================

    report_parser = subparsers.add_parser(
        "report",
        help="Generate a progress report",
    )

    report_parser.add_argument(
        "--format",
        choices=[
            "txt",
            "json",
            "csv",
            "all",
        ],
        default="txt",
        help="Report format",
    )

    return parser


def print_problem(problem) -> None:
    """Print one problem in a readable format."""

    solved_date = (
        problem["date_solved"]
        if problem["date_solved"]
        else "Not recorded"
    )

    next_revision = (
        problem["next_revision"]
        if problem["next_revision"]
        else "Not scheduled"
    )

    print(
        f"[{problem['id']}] "
        f"{problem['title']} | "
        f"{problem['topic']} | "
        f"{problem['difficulty']} | "
        f"{problem['platform']} | "
        f"{problem['status']} | "
        f"Solved: {solved_date} | "
        f"Next revision: {next_revision}"
    )


def handle_add(args) -> None:
    """Handle the add command."""

    manager = ProblemManager()

    problem_id = manager.add_problem(
        title=args.title,
        topic=args.topic,
        difficulty=args.difficulty,
        platform=args.platform,
        status=args.status,
        date_solved=args.date_solved,
    )

    logger.info(
        "Problem added successfully: ID=%s",
        problem_id,
    )

    print(
        f"Problem added successfully. "
        f"Problem ID: {problem_id}"
    )


def handle_list(args) -> None:
    """Handle the list command."""

    manager = ProblemManager()

    problems = manager.list_problems(
        search=args.search,
        topic=args.topic,
        difficulty=args.difficulty,
        status=args.status,
        platform=args.platform,
    )

    if not problems:
        print("No problems found.")
        return

    for problem in problems:
        print_problem(problem)

    print(
        f"\nTotal: {len(problems)}"
    )


def handle_view(args) -> None:
    """Handle the view command."""

    manager = ProblemManager()

    problem = manager.get_problem(
        args.id
    )

    print_problem(problem)

    history = manager.get_revision_history(
        args.id
    )

    print("\nRevision History:")

    if not history:
        print("No revisions recorded.")
        return

    for revision in history:
        print(
            f"- {revision['revised_on']} | "
            f"{revision['rating']}"
        )


def handle_update(args) -> None:
    """Handle the update command."""

    manager = ProblemManager()

    updated = manager.update_problem(
        problem_id=args.id,
        title=args.title,
        topic=args.topic,
        difficulty=args.difficulty,
        platform=args.platform,
        status=args.status,
        date_solved=args.date_solved,
    )

    if updated:
        logger.info(
            "Problem updated successfully: ID=%s",
            args.id,
        )

        print(
            f"Problem {args.id} "
            f"updated successfully."
        )

    else:
        print("No changes were made.")


def handle_delete(args) -> None:
    """Handle the delete command."""

    manager = ProblemManager()

    deleted = manager.delete_problem(
        args.id
    )

    if deleted:
        logger.info(
            "Problem deleted: ID=%s",
            args.id,
        )

        print(
            f"Problem {args.id} "
            f"deleted successfully."
        )

    else:
        print(
            "Problem could not be deleted."
        )


def handle_stats() -> None:
    """Handle the stats command."""

    analytics = Analytics()

    summary = analytics.summary()

    print("\nDSA PROGRESS SUMMARY")
    print("=" * 40)

    print(
        f"Total Problems: "
        f"{summary['total_problems']}"
    )

    print("\nStatus:")

    for status, count in (
        summary["status_distribution"].items()
    ):
        print(
            f"  {status}: {count}"
        )

    print("\nDifficulty:")

    for difficulty, count in (
        summary["difficulty_distribution"].items()
    ):
        print(
            f"  {difficulty}: {count}"
        )

    print("\nTopics:")

    if summary["topic_distribution"]:
        for topic, count in (
            summary["topic_distribution"].items()
        ):
            print(
                f"  {topic}: {count}"
            )

    else:
        print("  No data")

    print("\nWeekly Progress:")

    for week, count in (
        summary["weekly_progress"].items()
    ):
        print(
            f"  Week starting {week}: "
            f"{count} solved"
        )

    print(
        f"\nCurrent Streak: "
        f"{summary['current_streak']} day(s)"
    )

    print(
        f"Longest Streak: "
        f"{summary['longest_streak']} day(s)"
    )

    print("\nWeak Topics:")

    if summary["weak_topics"]:
        for item in summary["weak_topics"]:
            print(
                f"  {item['topic']}: "
                f"{item['solved']} solved"
            )

    else:
        print("  None identified")


def handle_due(args) -> None:
    """Handle the due command."""

    scheduler = RevisionScheduler()

    problems = scheduler.get_due_revisions(
        on_date=args.date
    )

    if not problems:
        print(
            "No revisions are due."
        )
        return

    print("DUE REVISIONS")
    print("=" * 40)

    for problem in problems:
        print(
            f"[{problem['id']}] "
            f"{problem['title']} | "
            f"{problem['topic']} | "
            f"Due: {problem['next_revision']}"
        )

    print(
        f"\nTotal due: {len(problems)}"
    )


def handle_upcoming(args) -> None:
    """Handle the upcoming command."""

    scheduler = RevisionScheduler()

    problems = scheduler.get_upcoming_revisions(
        days=args.days
    )

    if not problems:
        print(
            f"No revisions scheduled in "
            f"the next {args.days} day(s)."
        )
        return

    print(
        f"UPCOMING REVISIONS — "
        f"NEXT {args.days} DAYS"
    )

    print("=" * 40)

    for problem in problems:
        print(
            f"[{problem['id']}] "
            f"{problem['title']} | "
            f"Due: {problem['next_revision']}"
        )

    print(
        f"\nTotal upcoming: {len(problems)}"
    )


def handle_revise(args) -> None:
    """Handle the revise command."""

    scheduler = RevisionScheduler()

    result = scheduler.mark_revised(
        problem_id=args.id,
        rating=args.rating,
        revised_on=args.date,
    )

    logger.info(
        "Revision recorded: ID=%s, rating=%s",
        args.id,
        args.rating,
    )

    print(
        "Revision recorded successfully."
    )

    print(
        f"Problem: {result['title']}"
    )

    print(
        f"Rating: {result['rating']}"
    )

    print(
        f"Revision Level: "
        f"{result['revision_count']}"
    )

    print(
        f"Next Revision: "
        f"{result['next_revision']}"
    )


def handle_history(args) -> None:
    """Handle the history command."""

    manager = ProblemManager()

    history = manager.get_revision_history(
        args.id
    )

    if not history:
        print(
            "No revision history found."
        )
        return

    print(
        f"REVISION HISTORY — "
        f"PROBLEM {args.id}"
    )

    print("=" * 40)

    for revision in history:
        print(
            f"{revision['revised_on']} | "
            f"{revision['rating']}"
        )


def handle_import(args) -> None:
    """Handle JSON problem import."""

    manager = ProblemManager()

    try:
        with open(
            args.file,
            "r",
            encoding="utf-8",
        ) as file:
            problems = json.load(file)

    except FileNotFoundError:
        raise ValueError(
            f"Import file not found: {args.file}"
        )

    except json.JSONDecodeError:
        raise ValueError(
            "The import file contains invalid JSON."
        )

    if not isinstance(problems, list):
        raise ValueError(
            "Import JSON must contain "
            "a list of problems."
        )

    imported_count = manager.import_problems(
        problems
    )

    logger.info(
        "Imported %s problems from %s",
        imported_count,
        args.file,
    )

    print(
        f"Successfully imported "
        f"{imported_count} problem(s)."
    )


def handle_report(args) -> None:
    """Handle the report command."""

    reporter = Reporter()

    if args.format == "txt":

        path = reporter.export_txt()

        print(
            f"TXT report generated:\n{path}"
        )

    elif args.format == "json":

        path = reporter.export_json()

        print(
            f"JSON report generated:\n{path}"
        )

    elif args.format == "csv":

        path = reporter.export_csv()

        print(
            f"CSV report generated:\n{path}"
        )

    else:

        paths = reporter.export_all()

        print(
            "Reports generated successfully:"
        )

        for report_format, path in (
            paths.items()
        ):
            print(
                f"  {report_format.upper()}: "
                f"{path}"
            )


def main() -> None:
    """Application entry point."""

    setup_logging()

    parser = build_parser()

    args = parser.parse_args()

    try:

        if args.command == "add":
            handle_add(args)

        elif args.command == "list":
            handle_list(args)

        elif args.command == "view":
            handle_view(args)

        elif args.command == "update":
            handle_update(args)

        elif args.command == "delete":
            handle_delete(args)

        elif args.command == "stats":
            handle_stats()

        elif args.command == "due":
            handle_due(args)

        elif args.command == "upcoming":
            handle_upcoming(args)

        elif args.command == "revise":
            handle_revise(args)

        elif args.command == "history":
            handle_history(args)

        elif args.command == "import":
            handle_import(args)

        elif args.command == "report":
            handle_report(args)

    except ValueError as error:

        logger.error(
            "%s",
            error,
        )

        print(f"Error: {error}")
        raise SystemExit(1)

    except Exception as error:

        logger.exception(
            "Unexpected application error"
        )

        print(
            "An unexpected error occurred. "
            "Check logs/dsa_tracker.log for details."
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()