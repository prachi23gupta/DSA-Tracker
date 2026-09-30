import sqlite3
from pathlib import Path
from typing import Optional


DATABASE_PATH = Path(__file__).resolve().parent.parent / "dsa_tracker.db"


class Database:
    """Handles all SQLite database operations for the DSA Tracker."""

    def __init__(self, database_path: Path = DATABASE_PATH):
        self.database_path = database_path
        self.initialize_database()

    def get_connection(self):
        """Create and return a SQLite database connection."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize_database(self):
        """Create required database tables and indexes."""
        with self.get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    status TEXT NOT NULL,
                    date_solved TEXT,
                    revision_count INTEGER NOT NULL DEFAULT 0,
                    next_revision TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS revision_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem_id INTEGER NOT NULL,
                    revised_on TEXT NOT NULL,
                    rating TEXT NOT NULL,
                    FOREIGN KEY (problem_id)
                        REFERENCES problems(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_problems_topic
                ON problems(topic)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_problems_next_revision
                ON problems(next_revision)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_revision_log_problem
                ON revision_log(problem_id)
                """
            )

            connection.commit()

    def add_problem(
        self,
        title: str,
        topic: str,
        difficulty: str,
        platform: str,
        status: str,
        date_solved: Optional[str] = None,
        revision_count: int = 0,
        next_revision: Optional[str] = None,
    ) -> int:
        """Insert a new problem and return its generated ID."""

        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO problems (
                    title,
                    topic,
                    difficulty,
                    platform,
                    status,
                    date_solved,
                    revision_count,
                    next_revision
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    topic,
                    difficulty,
                    platform,
                    status,
                    date_solved,
                    revision_count,
                    next_revision,
                ),
            )

            connection.commit()
            return cursor.lastrowid

    def get_problem(self, problem_id: int):
        """Return one problem by ID."""
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT *
                FROM problems
                WHERE id = ?
                """,
                (problem_id,),
            )

            return cursor.fetchone()

    def get_all_problems(self):
        """Return all problems ordered by ID."""
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT *
                FROM problems
                ORDER BY id
                """
            )

            return cursor.fetchall()

    def find_by_title(self, title: str):
        """Find problems with an exact title."""
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT *
                FROM problems
                WHERE LOWER(title) = LOWER(?)
                """,
                (title,),
            )

            return cursor.fetchall()

    def update_problem(self, problem_id: int, **fields) -> bool:
        """Update selected fields of a problem."""

        allowed_fields = {
            "title",
            "topic",
            "difficulty",
            "platform",
            "status",
            "date_solved",
            "revision_count",
            "next_revision",
        }

        updates = {
            key: value
            for key, value in fields.items()
            if key in allowed_fields
        }

        if not updates:
            return False

        set_clause = ", ".join(
            f"{field} = ?" for field in updates
        )

        values = list(updates.values())
        values.append(problem_id)

        with self.get_connection() as connection:
            cursor = connection.execute(
                f"""
                UPDATE problems
                SET {set_clause}
                WHERE id = ?
                """,
                values,
            )

            connection.commit()
            return cursor.rowcount > 0

    def delete_problem(self, problem_id: int) -> bool:
        """Delete a problem by ID."""
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM problems
                WHERE id = ?
                """,
                (problem_id,),
            )

            connection.commit()
            return cursor.rowcount > 0

    def add_revision(
        self,
        problem_id: int,
        revised_on: str,
        rating: str,
    ) -> int:
        """Record a revision attempt."""

        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO revision_log (
                    problem_id,
                    revised_on,
                    rating
                )
                VALUES (?, ?, ?)
                """,
                (
                    problem_id,
                    revised_on,
                    rating,
                ),
            )

            connection.commit()
            return cursor.lastrowid

    def get_revision_history(self, problem_id: int):
        """Return revision history for a problem."""
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT *
                FROM revision_log
                WHERE problem_id = ?
                ORDER BY revised_on DESC, id DESC
                """,
                (problem_id,),
            )

            return cursor.fetchall()