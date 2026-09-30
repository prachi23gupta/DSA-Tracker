from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from typing import Optional

from .storage import Database


class Analytics:
    """Calculates progress and performance statistics."""

    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()

    def _get_problems(self):
        """Return all stored problems."""
        return self.database.get_all_problems()

    def total_problems(self) -> int:
        """Return total number of tracked problems."""
        return len(self._get_problems())

    def status_distribution(self) -> dict:
        """Return problem counts grouped by status."""
        problems = self._get_problems()

        counts = Counter(
            problem["status"]
            for problem in problems
        )

        return {
            "Solved": counts.get("Solved", 0),
            "Attempted": counts.get("Attempted", 0),
            "Unsolved": counts.get("Unsolved", 0),
        }

    def difficulty_distribution(self) -> dict:
        """Return problem counts grouped by difficulty."""
        problems = self._get_problems()

        counts = Counter(
            problem["difficulty"]
            for problem in problems
        )

        return {
            "Easy": counts.get("Easy", 0),
            "Medium": counts.get("Medium", 0),
            "Hard": counts.get("Hard", 0),
        }

    def topic_distribution(self) -> dict:
        """Return problem counts grouped by topic."""
        problems = self._get_problems()

        counts = Counter(
            problem["topic"]
            for problem in problems
        )

        return dict(
            sorted(
                counts.items(),
                key=lambda item: (-item[1], item[0])
            )
        )

    def solved_topic_distribution(self) -> dict:
        """Return solved problem counts grouped by topic."""
        problems = self._get_problems()

        counts = Counter(
            problem["topic"]
            for problem in problems
            if problem["status"] == "Solved"
        )

        return dict(
            sorted(
                counts.items(),
                key=lambda item: (-item[1], item[0])
            )
        )

    def weekly_progress(
        self,
        weeks: int = 8,
    ) -> dict:
        """
        Return solved-problem counts for the last N calendar weeks.

        The result uses ISO week labels.
        """

        if weeks <= 0:
            raise ValueError("Number of weeks must be positive.")

        problems = self._get_problems()

        today = date.today()

        current_monday = (
            today - timedelta(days=today.weekday())
        )

        weekly_counts = defaultdict(int)

        for problem in problems:
            if problem["status"] != "Solved":
                continue

            if not problem["date_solved"]:
                continue

            try:
                solved_date = datetime.strptime(
                    problem["date_solved"],
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                continue

            monday = (
                solved_date
                - timedelta(days=solved_date.weekday())
            )

            difference = (
                current_monday - monday
            ).days // 7

            if 0 <= difference < weeks:
                label = monday.strftime("%Y-%m-%d")
                weekly_counts[label] += 1

        result = {}

        for index in range(weeks - 1, -1, -1):
            monday = current_monday - timedelta(
                weeks=index
            )

            label = monday.strftime("%Y-%m-%d")
            result[label] = weekly_counts.get(label, 0)

        return result

    def _solved_dates(self):
        """Return unique dates on which problems were solved."""
        problems = self._get_problems()

        dates = set()

        for problem in problems:
            if problem["status"] != "Solved":
                continue

            if not problem["date_solved"]:
                continue

            try:
                solved_date = datetime.strptime(
                    problem["date_solved"],
                    "%Y-%m-%d",
                ).date()

                dates.add(solved_date)

            except ValueError:
                continue

        return dates

    def current_streak(self) -> int:
        """
        Return the number of consecutive days with
        at least one solved problem ending today or yesterday.
        """

        solved_dates = self._solved_dates()

        if not solved_dates:
            return 0

        today = date.today()

        if today not in solved_dates:
            if today - timedelta(days=1) not in solved_dates:
                return 0

            current_day = today - timedelta(days=1)
        else:
            current_day = today

        streak = 0

        while current_day in solved_dates:
            streak += 1
            current_day -= timedelta(days=1)

        return streak

    def longest_streak(self) -> int:
        """Return the longest consecutive solving streak."""

        solved_dates = sorted(self._solved_dates())

        if not solved_dates:
            return 0

        longest = 1
        current = 1

        for index in range(1, len(solved_dates)):
            difference = (
                solved_dates[index]
                - solved_dates[index - 1]
            ).days

            if difference == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        return longest

    def weak_topics(self, minimum_solved: int = 2) -> list:
        """
        Identify topics with comparatively low solved counts.

        Topics with fewer than minimum_solved solved problems
        are considered weak.
        """

        if minimum_solved < 1:
            raise ValueError(
                "Minimum solved count must be at least 1."
            )

        solved_by_topic = self.solved_topic_distribution()

        all_topics = {
            problem["topic"]
            for problem in self._get_problems()
        }

        weak = []

        for topic in sorted(all_topics):
            solved_count = solved_by_topic.get(topic, 0)

            if solved_count < minimum_solved:
                weak.append(
                    {
                        "topic": topic,
                        "solved": solved_count,
                    }
                )

        return weak

    def summary(self) -> dict:
        """Return a complete analytics summary."""

        status = self.status_distribution()
        difficulty = self.difficulty_distribution()

        return {
            "total_problems": self.total_problems(),
            "status_distribution": status,
            "difficulty_distribution": difficulty,
            "topic_distribution": self.topic_distribution(),
            "solved_topic_distribution": (
                self.solved_topic_distribution()
            ),
            "weekly_progress": self.weekly_progress(),
            "current_streak": self.current_streak(),
            "longest_streak": self.longest_streak(),
            "weak_topics": self.weak_topics(),
        }