from datetime import date, datetime, timedelta
from typing import Optional

from .storage import Database


REVISION_INTERVALS = [1, 3, 7, 14, 30]

RATING_EFFECTS = {
    "again": "reset",
    "hard": "repeat",
    "good": "advance",
    "easy": "advance",
}


class RevisionScheduler:
    """
    Manages spaced-repetition based revision scheduling.

    The schedule uses fixed intervals of:
    1, 3, 7, 14 and 30 days.
    """

    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()

    def _calculate_next_revision(
        self,
        revision_count: int,
        rating: str,
        revised_on: date,
    ) -> tuple[int, str]:
        """Calculate the next revision count and date."""

        rating = rating.strip().lower()

        if rating not in RATING_EFFECTS:
            raise ValueError(
                "Rating must be again, hard, good, or easy."
            )

        if rating == "again":
            new_count = 0
            interval = REVISION_INTERVALS[0]

        elif rating == "hard":
            new_count = min(
                revision_count,
                len(REVISION_INTERVALS) - 1,
            )
            interval = REVISION_INTERVALS[new_count]

        else:
            new_count = min(
                revision_count + 1,
                len(REVISION_INTERVALS) - 1,
            )
            interval = REVISION_INTERVALS[new_count]

        next_revision = (
            revised_on + timedelta(days=interval)
        ).isoformat()

        return new_count, next_revision

    def mark_revised(
        self,
        problem_id: int,
        rating: str,
        revised_on: Optional[str] = None,
    ) -> dict:
        """
        Mark a problem as revised and calculate its next revision.
        """

        problem = self.database.get_problem(problem_id)

        if problem is None:
            raise ValueError(
                f"No problem found with ID {problem_id}."
            )

        rating = rating.strip().lower()

        if rating not in RATING_EFFECTS:
            raise ValueError(
                "Rating must be again, hard, good, or easy."
            )

        if revised_on is None:
            revision_date = date.today()
        else:
            try:
                revision_date = datetime.strptime(
                    revised_on,
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                raise ValueError(
                    "Revision date must be in YYYY-MM-DD format."
                )

        new_count, next_revision = (
            self._calculate_next_revision(
                problem["revision_count"],
                rating,
                revision_date,
            )
        )

        self.database.add_revision(
            problem_id=problem_id,
            revised_on=revision_date.isoformat(),
            rating=rating,
        )

        self.database.update_problem(
            problem_id,
            revision_count=new_count,
            next_revision=next_revision,
        )

        return {
            "problem_id": problem_id,
            "title": problem["title"],
            "rating": rating,
            "revision_count": new_count,
            "next_revision": next_revision,
        }

    def get_due_revisions(
        self,
        on_date: Optional[str] = None,
    ):
        """Return all problems whose revision date is due."""

        if on_date is None:
            target_date = date.today()
        else:
            try:
                target_date = datetime.strptime(
                    on_date,
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                raise ValueError(
                    "Date must be in YYYY-MM-DD format."
                )

        problems = self.database.get_all_problems()

        due_problems = []

        for problem in problems:
            next_revision = problem["next_revision"]

            if not next_revision:
                continue

            try:
                revision_date = datetime.strptime(
                    next_revision,
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                continue

            if revision_date <= target_date:
                due_problems.append(problem)

        due_problems.sort(
            key=lambda problem: (
                problem["next_revision"],
                problem["id"],
            )
        )

        return due_problems

    def get_upcoming_revisions(
        self,
        days: int = 7,
        from_date: Optional[str] = None,
    ):
        """Return revisions scheduled within the next N days."""

        if days <= 0:
            raise ValueError(
                "Number of days must be positive."
            )

        if from_date is None:
            start_date = date.today()
        else:
            try:
                start_date = datetime.strptime(
                    from_date,
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                raise ValueError(
                    "Date must be in YYYY-MM-DD format."
                )

        end_date = start_date + timedelta(days=days)

        problems = self.database.get_all_problems()

        upcoming = []

        for problem in problems:
            next_revision = problem["next_revision"]

            if not next_revision:
                continue

            try:
                revision_date = datetime.strptime(
                    next_revision,
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                continue

            if start_date <= revision_date <= end_date:
                upcoming.append(problem)

        upcoming.sort(
            key=lambda problem: (
                problem["next_revision"],
                problem["id"],
            )
        )

        return upcoming