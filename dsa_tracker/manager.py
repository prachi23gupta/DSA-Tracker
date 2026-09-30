from datetime import date, timedelta
from typing import Optional

from .storage import Database
from .validators import (
    validate_date,
    validate_difficulty,
    validate_platform,
    validate_status,
    validate_title,
    validate_topic,
)


class ProblemManager:
    """Business logic for managing DSA problems."""

    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()

    def add_problem(
        self,
        title: str,
        topic: str,
        difficulty: str,
        platform: str = "LeetCode",
        status: str = "Solved",
        date_solved: Optional[str] = None,
    ) -> int:
        """Validate and add a new DSA problem."""

        title = validate_title(title)
        topic = validate_topic(topic)
        difficulty = validate_difficulty(difficulty)
        platform = validate_platform(platform)
        status = validate_status(status)

        if date_solved:
            date_solved = validate_date(date_solved)
        elif status == "Solved":
            date_solved = date.today().isoformat()

        if status == "Solved" and not date_solved:
            raise ValueError("Solved problems must have a solve date.")

        if status != "Solved" and date_solved:
            raise ValueError(
                "Only Solved problems can have a solve date."
            )

        next_revision = None
        if status == "Solved":
            next_revision = (
                date.fromisoformat(date_solved)
                + timedelta(days=1)
            ).isoformat()

        existing_problem = self.database.find_by_title(title)

        if existing_problem:
            raise ValueError(
                f"A problem with the title "
                f"'{title}' already exists."
            )

        return self.database.add_problem(
            title=title,
            topic=topic,
            difficulty=difficulty,
            platform=platform,
            status=status,
            date_solved=date_solved,
            next_revision=next_revision,
        )

    def get_problem(self, problem_id: int):
        """Get one problem by ID."""

        problem = self.database.get_problem(problem_id)

        if problem is None:
            raise ValueError(
                f"No problem found with ID {problem_id}."
            )

        return problem

    def list_problems(
        self,
        search: Optional[str] = None,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        status: Optional[str] = None,
        platform: Optional[str] = None,
    ):
        """
        Return problems matching optional search and filters.

        Search performs a case-insensitive partial match
        against the problem title.
        """

        problems = self.database.get_all_problems()

        if search:
            search = search.strip().lower()

            problems = [
                problem
                for problem in problems
                if search in problem["title"].lower()
            ]

        if topic:
            topic = topic.strip().lower()

            problems = [
                problem
                for problem in problems
                if problem["topic"].lower() == topic
            ]

        if difficulty:
            difficulty = validate_difficulty(
                difficulty
            )

            problems = [
                problem
                for problem in problems
                if problem["difficulty"] == difficulty
            ]

        if status:
            status = validate_status(status)

            problems = [
                problem
                for problem in problems
                if problem["status"] == status
            ]

        if platform:
            platform = platform.strip().lower()

            problems = [
                problem
                for problem in problems
                if problem["platform"].lower() == platform
            ]

        return problems

    def update_problem(
        self,
        problem_id: int,
        title: Optional[str] = None,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        date_solved: Optional[str] = None,
    ) -> bool:
        """Validate and update selected problem fields."""

        current_problem = self.get_problem(problem_id)

        updates = {}

        if title is not None:
            updates["title"] = validate_title(title)

        if topic is not None:
            updates["topic"] = validate_topic(topic)

        if difficulty is not None:
            updates["difficulty"] = validate_difficulty(
                difficulty
            )

        if platform is not None:
            updates["platform"] = validate_platform(
                platform
            )

        if status is not None:
            updates["status"] = validate_status(
                status
            )

        if date_solved is not None:
            updates["date_solved"] = validate_date(
                date_solved
            )

        if "title" in updates:
            duplicates = self.database.find_by_title(
                updates["title"]
            )

            for problem in duplicates:
                if problem["id"] != problem_id:
                    raise ValueError(
                        f"A problem with the title "
                        f"'{updates['title']}' already exists."
                    )

        if not updates:
            raise ValueError(
                "At least one field must be provided "
                "for update."
            )

        resulting_status = updates.get(
            "status", current_problem["status"]
        )
        resulting_date = updates.get(
            "date_solved", current_problem["date_solved"]
        )

        if resulting_status == "Solved" and not resulting_date:
            resulting_date = date.today().isoformat()
            updates["date_solved"] = resulting_date

        if resulting_status != "Solved" and resulting_date:
            if "date_solved" in updates:
                raise ValueError(
                    "Only Solved problems can have a solve date."
                )
            updates["date_solved"] = None

        if resulting_status == "Solved" and resulting_date:
            updates["next_revision"] = (
                date.fromisoformat(resulting_date)
                + timedelta(days=1)
            ).isoformat()

        elif resulting_status != "Solved":
            updates["next_revision"] = None

        return self.database.update_problem(
            problem_id,
            **updates,
        )

    def delete_problem(
        self,
        problem_id: int,
    ) -> bool:
        """Delete a problem after confirming it exists."""

        self.get_problem(problem_id)

        return self.database.delete_problem(
            problem_id
        )

    def add_revision(
        self,
        problem_id: int,
        revised_on: str,
        rating: str,
    ) -> int:
        """Record a revision for an existing problem."""

        self.get_problem(problem_id)

        revised_on = validate_date(revised_on)

        rating = rating.strip().lower()

        valid_ratings = {
            "hard",
            "again",
            "good",
            "easy",
        }

        if rating not in valid_ratings:
            raise ValueError(
                "Revision rating must be hard, "
                "again, good, or easy."
            )

        return self.database.add_revision(
            problem_id=problem_id,
            revised_on=revised_on,
            rating=rating,
        )

    def get_revision_history(
        self,
        problem_id: int,
    ):
        """Return revision history for a problem."""

        self.get_problem(problem_id)

        return self.database.get_revision_history(
            problem_id
        )

    def import_problems(
        self,
        problems: list,
    ) -> int:
        """
        Import multiple problems into the database.

        Invalid or duplicate records are skipped so
        that one bad record does not stop the complete
        import.
        """

        if not isinstance(problems, list):
            raise ValueError(
                "Import data must be a list of problems."
            )

        imported_count = 0

        for problem in problems:

            if not isinstance(problem, dict):
                continue

            try:
                self.add_problem(
                    title=problem["title"],
                    topic=problem["topic"],
                    difficulty=problem["difficulty"],
                    platform=problem.get(
                        "platform",
                        "LeetCode",
                    ),
                    status=problem.get(
                        "status",
                        "Unsolved",
                    ),
                    date_solved=problem.get(
                        "date_solved"
                    ),
                )

                imported_count += 1

            except (
                KeyError,
                TypeError,
                ValueError,
            ):
                continue

        return imported_count