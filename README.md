# DSA Progress & Revision Analyzer

A command-line Python application for tracking DSA problems, analyzing coding progress, and scheduling spaced-repetition revisions.

## Features

- Add, update, delete and view DSA problems
- Search and filter problems by title, topic, difficulty, status and platform
- Track Solved, Attempted and Unsolved problems
- Validate solve dates and status/date consistency
- Topic-wise and difficulty-wise analytics
- Weekly progress tracking
- Current and longest solving streak
- Weak-topic identification
- Spaced-repetition revision scheduling using 1, 3, 7, 14 and 30-day intervals
- Automatic first revision scheduling one day after a problem is solved
- Revision ratings: again, hard, good and easy
- Due and upcoming revision tracking
- Revision history
- TXT, JSON and CSV report generation
- JSON sample-data import
- SQLite persistent storage
- File-based application logging
- Automated pytest test suite

## Project Architecture

```text
User
  |
  v
CLI (main.py)
  |
  +-------------------+
  |                   |
  v                   v
Problem Manager    Revision Scheduler
  |                   |
  v                   v
Validators         Revision Logic
  |                   |
  +---------+---------+
            |
            v
       SQLite Storage
            |
      +-----+-----+
      |           |
      v           v
  Problems    Revision Log
      |
      v
   Analytics
      |
      +----------+
      |          |
      v          v
 Reporter     CLI Output
```

## Project Structure

```text
DSA-Tracker/
├── dsa_tracker/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   ├── manager.py
│   ├── analytics.py
│   ├── scheduler.py
│   ├── reporter.py
│   ├── validators.py
│   └── logger_config.py
├── tests/
│   ├── __init__.py
│   ├── test_manager.py
│   ├── test_analytics.py
│   └── test_scheduler.py
├── sample_data/
│   ├── generate_sample.py
│   └── sample_problems.json
├── docs/
│   ├── architecture.png
│   ├── er_diagram.png
│   ├── revision_workflow.png
│   ├── use_case.png
│   └── generate_diagrams.py
├── reports/
│   └── .gitkeep
├── README.md
├── statement.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- SQLite (included with Python)
- pytest for testing

The application runtime uses Python's standard library. The only external development/test dependency is `pytest`.

## Setup

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Show available commands:

```bash
python -m dsa_tracker --help
```

Import the sample dataset:

```bash
python -m dsa_tracker import --file sample_data/sample_problems.json
```

View analytics:

```bash
python -m dsa_tracker stats
```

Add a problem:

```bash
python -m dsa_tracker add --title "Two Sum" --topic Arrays --difficulty Easy --status Solved --date-solved 2026-09-29
```

Record a revision:

```bash
python -m dsa_tracker revise --id 1 --rating good
```

Check revisions:

```bash
python -m dsa_tracker due
python -m dsa_tracker upcoming
python -m dsa_tracker history --id 1
```

Generate reports:

```bash
python -m dsa_tracker report --format all
```

Run tests:

```bash
pytest
```

## Demo Workflow

For a clean demonstration, start with a fresh database or remove the existing `dsa_tracker.db` before importing the sample data.

```bash
python -m dsa_tracker import --file sample_data/sample_problems.json
python -m dsa_tracker stats
python -m dsa_tracker due
python -m dsa_tracker upcoming
python -m dsa_tracker revise --id 1 --rating good
python -m dsa_tracker history --id 1
python -m dsa_tracker report --format all
```

The sample dataset contains solved, attempted and unsolved problems. Solved problems receive an initial revision date one day after their solve date, so the `due` and `upcoming` commands demonstrate the revision scheduler immediately after import. The dataset also contains topics with fewer than two solved problems so the weak-topic analysis is visible.

## Validation and Error Handling

- Empty and overlong titles/topics/platforms are rejected.
- Difficulty and status values are validated.
- Dates must use `YYYY-MM-DD` format and cannot be in the future when recording a solve or revision.
- A Solved problem always has a solve date.
- Attempted and Unsolved problems do not keep a solve date.
- Duplicate problem titles are rejected.
- Invalid commands return a non-zero exit code.
- Application errors are recorded in `logs/dsa_tracker.log` while normal CLI output remains clean.

## Revision Scheduling

The revision scheduler uses fixed spaced-repetition intervals:

| Revision level | Next interval |
|---|---:|
| Initial revision | 1 day |
| Level 1 | 3 days |
| Level 2 | 7 days |
| Level 3 | 14 days |
| Level 4 | 30 days |

`again` resets the revision level, while `hard`, `good` and `easy` determine how the current level progresses according to the scheduler rules implemented in `scheduler.py`.

## Reports

The reporter can generate:

- TXT summary report
- JSON structured report
- CSV topic report

Generated report files are ignored by Git so local generated output does not clutter the repository.

## Database

SQLite stores two main entities:

1. `problems` — problem metadata, status, solve date and revision schedule.
2. `revision_log` — revision events linked to problems through a foreign key.

Indexes are created for topic, next revision date and revision history lookup.

## Testing

The project uses `pytest` with isolated temporary SQLite databases. Tests cover:

- Problem creation and validation
- Duplicate detection
- Search and filtering
- Updating and deleting problems
- JSON import
- Revision history
- Analytics calculations
- Streak calculations
- Weak-topic detection
- Revision scheduling
- Due and upcoming revision queries
- Invalid rating/date handling

## Non-Functional Requirements

- **Usability:** clear CLI commands and readable output.
- **Reliability:** validation, error handling and isolated automated tests.
- **Maintainability:** modular Python package structure with separate business, storage, analytics and scheduling layers.
- **Performance:** SQLite indexes and lightweight standard-library implementation.
- **Portability:** runs on systems with Python 3.10+ and SQLite.
- **Testability:** business logic is separated from CLI handling and tested with temporary databases.

## Design Decisions

- **SQLite:** provides persistent local storage without requiring a separate database server.
- **Layered architecture:** separates CLI, business logic, scheduling, analytics and storage responsibilities.
- **Fixed spaced-repetition intervals:** keeps the scheduling logic deterministic and easy to understand.
- **Standard library runtime:** minimizes installation and deployment complexity.
- **Pytest:** provides repeatable automated verification of the main functional modules.

## Future Enhancements

- Interactive dashboard and charts
- Import/export support for additional formats
- User-configurable revision intervals
- More detailed performance trends
- Cloud synchronization
- Authentication for multi-user deployments

## Project Statement

See [`statement.md`](statement.md) for the detailed problem statement, scope and objectives.

## License

This project is developed as an academic course project.
