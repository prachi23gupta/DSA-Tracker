from datetime import date, datetime


VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
VALID_STATUSES = {"Solved", "Attempted", "Unsolved"}


def validate_title(title: str) -> str:
    title = title.strip()

    if not title:
        raise ValueError("Problem title cannot be empty.")

    if len(title) > 150:
        raise ValueError("Problem title cannot exceed 150 characters.")

    return title


def validate_topic(topic: str) -> str:
    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    if len(topic) > 80:
        raise ValueError("Topic cannot exceed 80 characters.")

    return topic


def validate_difficulty(difficulty: str) -> str:
    difficulty = difficulty.strip().title()

    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError("Difficulty must be Easy, Medium, or Hard.")

    return difficulty


def validate_status(status: str) -> str:
    status = status.strip().title()

    if status not in VALID_STATUSES:
        raise ValueError("Status must be Solved, Attempted, or Unsolved.")

    return status


def validate_platform(platform: str) -> str:
    platform = platform.strip()

    if not platform:
        raise ValueError("Platform cannot be empty.")

    if len(platform) > 50:
        raise ValueError("Platform cannot exceed 50 characters.")

    return platform


def validate_date(date_value: str) -> str:
    try:
        parsed_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    if parsed_date > date.today():
        raise ValueError("Date cannot be in the future.")

    return date_value
