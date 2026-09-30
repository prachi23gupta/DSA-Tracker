import pytest

from dsa_tracker.scheduler import RevisionScheduler
from dsa_tracker.storage import Database


@pytest.fixture
def scheduler(tmp_path):
    database = Database(tmp_path / "scheduler.db")

    database.add_problem(
        "Two Sum",
        "Arrays",
        "Easy",
        "LeetCode",
        "Solved",
        "2026-09-25",
    )

    database.add_problem(
        "Binary Search",
        "Searching",
        "Easy",
        "LeetCode",
        "Solved",
        "2026-09-25",
    )

    return RevisionScheduler(database)


def test_mark_revised_good(scheduler):
    result = scheduler.mark_revised(
        problem_id=1,
        rating="good",
        revised_on="2026-09-30",
    )

    assert result["revision_count"] == 1
    assert result["next_revision"] == "2026-10-03"


def test_mark_revised_easy_advances(scheduler):
    result = scheduler.mark_revised(
        problem_id=1,
        rating="easy",
        revised_on="2026-09-30",
    )

    assert result["revision_count"] == 1
    assert result["next_revision"] == "2026-10-03"


def test_again_resets_revision_level(scheduler):
    scheduler.mark_revised(
        problem_id=1,
        rating="good",
        revised_on="2026-09-30",
    )

    result = scheduler.mark_revised(
        problem_id=1,
        rating="again",
        revised_on="2026-10-03",
    )

    assert result["revision_count"] == 0
    assert result["next_revision"] == "2026-10-04"


def test_hard_keeps_current_level(scheduler):
    scheduler.mark_revised(
        problem_id=1,
        rating="good",
        revised_on="2026-09-30",
    )

    result = scheduler.mark_revised(
        problem_id=1,
        rating="hard",
        revised_on="2026-10-03",
    )

    assert result["revision_count"] == 1
    assert result["next_revision"] == "2026-10-06"


def test_invalid_rating(scheduler):
    with pytest.raises(ValueError):
        scheduler.mark_revised(
            problem_id=1,
            rating="excellent",
            revised_on="2026-09-30",
        )


def test_missing_problem(scheduler):
    with pytest.raises(ValueError):
        scheduler.mark_revised(
            problem_id=999,
            rating="good",
        )


def test_due_revisions(scheduler):
    scheduler.mark_revised(
        problem_id=1,
        rating="good",
        revised_on="2026-09-25",
    )

    due = scheduler.get_due_revisions(
        on_date="2026-10-03"
    )

    assert len(due) == 1
    assert due[0]["title"] == "Two Sum"


def test_upcoming_revisions(scheduler):
    scheduler.mark_revised(
        problem_id=1,
        rating="good",
        revised_on="2026-09-30",
    )

    upcoming = scheduler.get_upcoming_revisions(
        days=7,
        from_date="2026-09-30",
    )

    assert len(upcoming) == 1
    assert upcoming[0]["title"] == "Two Sum"


def test_invalid_upcoming_days(scheduler):
    with pytest.raises(ValueError):
        scheduler.get_upcoming_revisions(days=0)


def test_invalid_date(scheduler):
    with pytest.raises(ValueError):
        scheduler.mark_revised(
            problem_id=1,
            rating="good",
            revised_on="30-09-2026",
        )