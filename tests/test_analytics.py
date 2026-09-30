import pytest

from dsa_tracker.analytics import Analytics
from dsa_tracker.storage import Database


@pytest.fixture
def analytics(tmp_path):
    database = Database(tmp_path / "analytics.db")

    database.add_problem(
        "Two Sum", "Arrays", "Easy", "LeetCode",
        "Solved", "2026-09-25"
    )
    database.add_problem(
        "Binary Search", "Searching", "Easy", "LeetCode",
        "Solved", "2026-09-26"
    )
    database.add_problem(
        "Valid Parentheses", "Strings", "Easy", "LeetCode",
        "Solved", "2026-09-26"
    )
    database.add_problem(
        "Number of Islands", "Graphs", "Medium", "LeetCode",
        "Attempted", None
    )

    return Analytics(database)


def test_total_problems(analytics):
    assert analytics.total_problems() == 4


def test_status_distribution(analytics):
    result = analytics.status_distribution()

    assert result["Solved"] == 3
    assert result["Attempted"] == 1
    assert result["Unsolved"] == 0


def test_difficulty_distribution(analytics):
    result = analytics.difficulty_distribution()

    assert result["Easy"] == 3
    assert result["Medium"] == 1
    assert result["Hard"] == 0


def test_topic_distribution(analytics):
    result = analytics.topic_distribution()

    assert result["Arrays"] == 1
    assert result["Searching"] == 1
    assert result["Strings"] == 1
    assert result["Graphs"] == 1


def test_solved_topic_distribution(analytics):
    result = analytics.solved_topic_distribution()

    assert result["Arrays"] == 1
    assert result["Searching"] == 1
    assert result["Strings"] == 1
    assert "Graphs" not in result


def test_longest_streak(analytics):
    assert analytics.longest_streak() == 2


def test_current_streak(analytics):
    assert analytics.current_streak() == 0


def test_weak_topics(analytics):
    result = analytics.weak_topics(minimum_solved=2)

    topics = {item["topic"] for item in result}

    assert "Arrays" in topics
    assert "Searching" in topics
    assert "Strings" in topics
    assert "Graphs" in topics


def test_invalid_week_count(analytics):
    with pytest.raises(ValueError):
        analytics.weekly_progress(0)


def test_invalid_weak_topic_threshold(analytics):
    with pytest.raises(ValueError):
        analytics.weak_topics(0)


def test_summary(analytics):
    result = analytics.summary()

    assert result["total_problems"] == 4
    assert "status_distribution" in result
    assert "difficulty_distribution" in result
    assert "topic_distribution" in result
    assert "weekly_progress" in result
    assert "current_streak" in result
    assert "longest_streak" in result
    assert "weak_topics" in result
