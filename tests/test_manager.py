import pytest

from dsa_tracker.manager import ProblemManager
from dsa_tracker.storage import Database


@pytest.fixture
def manager(tmp_path):
    """Create an isolated test database."""
    database = Database(tmp_path / "test.db")
    return ProblemManager(database)


def test_add_problem(manager):
    problem_id = manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
        platform="LeetCode",
        status="Solved",
        date_solved="2026-09-25",
    )

    problem = manager.get_problem(problem_id)

    assert problem["title"] == "Two Sum"
    assert problem["topic"] == "Arrays"
    assert problem["difficulty"] == "Easy"
    assert problem["status"] == "Solved"
    assert problem["date_solved"] == "2026-09-25"


def test_solved_problem_gets_current_date(manager):
    problem_id = manager.add_problem(
        title="Binary Search",
        topic="Searching",
        difficulty="Easy",
        status="Solved",
    )

    problem = manager.get_problem(problem_id)

    assert problem["date_solved"] is not None


def test_duplicate_problem_is_rejected(manager):
    manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    with pytest.raises(ValueError):
        manager.add_problem(
            title="Two Sum",
            topic="Arrays",
            difficulty="Easy",
        )


def test_invalid_difficulty_is_rejected(manager):
    with pytest.raises(ValueError):
        manager.add_problem(
            title="Test Problem",
            topic="Arrays",
            difficulty="Very Hard",
        )


def test_invalid_title_is_rejected(manager):
    with pytest.raises(ValueError):
        manager.add_problem(
            title="",
            topic="Arrays",
            difficulty="Easy",
        )


def test_get_missing_problem_is_rejected(manager):
    with pytest.raises(ValueError):
        manager.get_problem(999)


def test_list_by_topic(manager):
    manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    manager.add_problem(
        title="Valid Parentheses",
        topic="Strings",
        difficulty="Easy",
    )

    problems = manager.list_problems(
        topic="Arrays"
    )

    assert len(problems) == 1
    assert problems[0]["title"] == "Two Sum"


def test_list_by_difficulty(manager):
    manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    manager.add_problem(
        title="Trapping Rain Water",
        topic="Arrays",
        difficulty="Hard",
    )

    problems = manager.list_problems(
        difficulty="Hard"
    )

    assert len(problems) == 1
    assert problems[0]["title"] == "Trapping Rain Water"


def test_search_by_title(manager):
    manager.add_problem(
        title="Binary Search",
        topic="Searching",
        difficulty="Easy",
    )

    manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    problems = manager.list_problems(
        search="binary"
    )

    assert len(problems) == 1
    assert problems[0]["title"] == "Binary Search"


def test_combined_filters(manager):
    manager.add_problem(
        title="Array Medium Problem",
        topic="Arrays",
        difficulty="Medium",
        status="Solved",
    )

    manager.add_problem(
        title="Array Easy Problem",
        topic="Arrays",
        difficulty="Easy",
        status="Solved",
    )

    problems = manager.list_problems(
        topic="Arrays",
        difficulty="Medium",
        status="Solved",
    )

    assert len(problems) == 1
    assert problems[0]["title"] == "Array Medium Problem"


def test_update_problem(manager):
    problem_id = manager.add_problem(
        title="Old Title",
        topic="Arrays",
        difficulty="Easy",
    )

    result = manager.update_problem(
        problem_id=problem_id,
        title="New Title",
        difficulty="Medium",
    )

    assert result is True

    problem = manager.get_problem(problem_id)

    assert problem["title"] == "New Title"
    assert problem["difficulty"] == "Medium"


def test_duplicate_title_during_update_is_rejected(manager):
    first_id = manager.add_problem(
        title="First Problem",
        topic="Arrays",
        difficulty="Easy",
    )

    manager.add_problem(
        title="Second Problem",
        topic="Strings",
        difficulty="Easy",
    )

    with pytest.raises(ValueError):
        manager.update_problem(
            problem_id=first_id,
            title="Second Problem",
        )


def test_update_without_fields_is_rejected(manager):
    problem_id = manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    with pytest.raises(ValueError):
        manager.update_problem(
            problem_id=problem_id
        )


def test_delete_problem(manager):
    problem_id = manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    result = manager.delete_problem(problem_id)

    assert result is True

    with pytest.raises(ValueError):
        manager.get_problem(problem_id)


def test_import_problems(manager):
    problems = [
        {
            "title": "Two Sum",
            "topic": "Arrays",
            "difficulty": "Easy",
            "platform": "LeetCode",
            "status": "Solved",
            "date_solved": "2026-09-25",
        },
        {
            "title": "Binary Search",
            "topic": "Searching",
            "difficulty": "Easy",
            "platform": "LeetCode",
            "status": "Solved",
            "date_solved": "2026-09-26",
        },
    ]

    imported = manager.import_problems(problems)

    assert imported == 2
    assert len(manager.list_problems()) == 2


def test_import_skips_duplicate(manager):
    manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    problems = [
        {
            "title": "Two Sum",
            "topic": "Arrays",
            "difficulty": "Easy",
        },
        {
            "title": "Binary Search",
            "topic": "Searching",
            "difficulty": "Easy",
        },
    ]

    imported = manager.import_problems(problems)

    assert imported == 1
    assert len(manager.list_problems()) == 2


def test_revision_history(manager):
    problem_id = manager.add_problem(
        title="Two Sum",
        topic="Arrays",
        difficulty="Easy",
    )

    manager.add_revision(
        problem_id=problem_id,
        revised_on="2026-09-30",
        rating="good",
    )

    history = manager.get_revision_history(
        problem_id
    )

    assert len(history) == 1
    assert history[0]["rating"] == "good"
    assert history[0]["revised_on"] == "2026-09-30"

def test_future_solve_date_is_rejected(manager):
    with pytest.raises(ValueError, match="future"):
        manager.add_problem(
            title="Future Problem",
            topic="Arrays",
            difficulty="Easy",
            status="Solved",
            date_solved="2030-01-01",
        )


def test_non_solved_problem_cannot_have_solve_date(manager):
    with pytest.raises(ValueError, match="Only Solved"):
        manager.add_problem(
            title="Unsolved Problem",
            topic="Arrays",
            difficulty="Easy",
            status="Unsolved",
            date_solved="2026-09-29",
        )


def test_changing_status_to_unsolved_clears_solve_date(manager):
    problem_id = manager.add_problem(
        title="Status Update",
        topic="Arrays",
        difficulty="Easy",
        status="Solved",
        date_solved="2026-09-29",
    )

    manager.update_problem(
        problem_id,
        status="Unsolved",
    )

    problem = manager.get_problem(problem_id)

    assert problem["status"] == "Unsolved"
    assert problem["date_solved"] is None
    assert problem["next_revision"] is None


def test_changing_status_to_solved_adds_date(manager):
    problem_id = manager.add_problem(
        title="Solve Later",
        topic="Arrays",
        difficulty="Easy",
        status="Unsolved",
    )

    manager.update_problem(
        problem_id,
        status="Solved",
    )

    problem = manager.get_problem(problem_id)

    assert problem["status"] == "Solved"
    assert problem["date_solved"] is not None
    assert problem["next_revision"] is not None
