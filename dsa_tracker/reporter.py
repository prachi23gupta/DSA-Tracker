import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .analytics import Analytics


REPORTS_DIRECTORY = (
    Path(__file__).resolve().parent.parent / "reports"
)


class Reporter:
    """Generates progress reports in TXT, JSON and CSV formats."""

    def __init__(
        self,
        analytics: Optional[Analytics] = None,
        output_directory: Optional[Path] = None,
    ):
        self.analytics = analytics or Analytics()

        self.output_directory = (
            output_directory or REPORTS_DIRECTORY
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _timestamp(self) -> str:
        """Return a timestamp suitable for filenames."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_report_data(self) -> dict:
        """Get the complete analytics summary."""
        return self.analytics.summary()

    def export_json(self) -> Path:
        """Export the analytics summary as JSON."""

        data = self._get_report_data()

        filename = (
            f"dsa_report_{self._timestamp()}.json"
        )

        output_path = self.output_directory / filename

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

        return output_path

    def export_txt(self) -> Path:
        """Export a human-readable text report."""

        data = self._get_report_data()

        filename = (
            f"dsa_report_{self._timestamp()}.txt"
        )

        output_path = self.output_directory / filename

        lines = [
            "DSA PROGRESS REPORT",
            "=" * 50,
            "",
            f"Total Problems: {data['total_problems']}",
            "",
            "STATUS DISTRIBUTION",
            "-" * 30,
        ]

        for status, count in (
            data["status_distribution"].items()
        ):
            lines.append(
                f"{status}: {count}"
            )

        lines.extend(
            [
                "",
                "DIFFICULTY DISTRIBUTION",
                "-" * 30,
            ]
        )

        for difficulty, count in (
            data["difficulty_distribution"].items()
        ):
            lines.append(
                f"{difficulty}: {count}"
            )

        lines.extend(
            [
                "",
                "TOPIC DISTRIBUTION",
                "-" * 30,
            ]
        )

        for topic, count in (
            data["topic_distribution"].items()
        ):
            lines.append(
                f"{topic}: {count}"
            )

        lines.extend(
            [
                "",
                "SOLVED PROBLEMS BY TOPIC",
                "-" * 30,
            ]
        )

        for topic, count in (
            data["solved_topic_distribution"].items()
        ):
            lines.append(
                f"{topic}: {count}"
            )

        lines.extend(
            [
                "",
                "WEEKLY PROGRESS",
                "-" * 30,
            ]
        )

        for week, count in (
            data["weekly_progress"].items()
        ):
            lines.append(
                f"Week starting {week}: {count} solved"
            )

        lines.extend(
            [
                "",
                "STREAKS",
                "-" * 30,
                f"Current Streak: "
                f"{data['current_streak']} day(s)",
                f"Longest Streak: "
                f"{data['longest_streak']} day(s)",
                "",
                "WEAK TOPICS",
                "-" * 30,
            ]
        )

        if data["weak_topics"]:
            for item in data["weak_topics"]:
                lines.append(
                    f"{item['topic']}: "
                    f"{item['solved']} solved"
                )
        else:
            lines.append(
                "No weak topics identified."
            )

        lines.extend(
            [
                "",
                "=" * 50,
            ]
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            file.write("\n".join(lines))

        return output_path

    def export_csv(self) -> Path:
        """
        Export topic-level analytics as CSV.

        Each row represents one topic.
        """

        filename = (
            f"dsa_topic_report_{self._timestamp()}.csv"
        )

        output_path = self.output_directory / filename

        topic_counts = (
            self.analytics.topic_distribution()
        )

        solved_counts = (
            self.analytics.solved_topic_distribution()
        )

        topics = sorted(
            set(topic_counts) | set(solved_counts)
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    "Topic",
                    "Total Problems",
                    "Solved Problems",
                ]
            )

            for topic in topics:
                writer.writerow(
                    [
                        topic,
                        topic_counts.get(topic, 0),
                        solved_counts.get(topic, 0),
                    ]
                )

        return output_path

    def export_all(self) -> dict:
        """Generate TXT, JSON and CSV reports."""

        return {
            "txt": self.export_txt(),
            "json": self.export_json(),
            "csv": self.export_csv(),
        }