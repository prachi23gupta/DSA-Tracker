import json
import random
from datetime import date, timedelta
from pathlib import Path


OUTPUT_FILE = (
    Path(__file__).resolve().parent
    / "sample_problems.json"
)


PROBLEM_BANK = [
    ("Two Sum", "Arrays", "Easy"),
    ("Best Time to Buy and Sell Stock", "Arrays", "Easy"),
    ("Contains Duplicate", "Arrays", "Easy"),
    ("Product of Array Except Self", "Arrays", "Medium"),
    ("Maximum Subarray", "Arrays", "Medium"),
    ("3Sum", "Arrays", "Medium"),
    ("Container With Most Water", "Arrays", "Medium"),
    ("Trapping Rain Water", "Arrays", "Hard"),
    ("Valid Parentheses", "Strings", "Easy"),
    ("Valid Anagram", "Strings", "Easy"),
    ("Longest Common Prefix", "Strings", "Easy"),
    ("Longest Substring Without Repeating Characters", "Strings", "Medium"),
    ("Group Anagrams", "Strings", "Medium"),
    ("Longest Palindromic Substring", "Strings", "Medium"),
    ("Minimum Window Substring", "Strings", "Hard"),
    ("Binary Search", "Searching", "Easy"),
    ("Search in Rotated Sorted Array", "Searching", "Medium"),
    ("Find Minimum in Rotated Sorted Array", "Searching", "Medium"),
    ("Koko Eating Bananas", "Searching", "Medium"),
    ("Median of Two Sorted Arrays", "Searching", "Hard"),
    ("Reverse Linked List", "Linked List", "Easy"),
    ("Merge Two Sorted Lists", "Linked List", "Easy"),
    ("Remove Nth Node From End of List", "Linked List", "Medium"),
    ("Reorder List", "Linked List", "Medium"),
    ("Merge K Sorted Lists", "Linked List", "Hard"),
    ("Valid Palindrome", "Two Pointers", "Easy"),
    ("Two Sum II", "Two Pointers", "Medium"),
    ("3Sum Closest", "Two Pointers", "Medium"),
    ("Move Zeroes", "Two Pointers", "Easy"),
    ("Climbing Stairs", "Dynamic Programming", "Easy"),
    ("House Robber", "Dynamic Programming", "Medium"),
    ("Coin Change", "Dynamic Programming", "Medium"),
    ("Longest Increasing Subsequence", "Dynamic Programming", "Medium"),
    ("Edit Distance", "Dynamic Programming", "Hard"),
    ("Maximum Product Subarray", "Dynamic Programming", "Medium"),
    ("Invert Binary Tree", "Trees", "Easy"),
    ("Maximum Depth of Binary Tree", "Trees", "Easy"),
    ("Binary Tree Level Order Traversal", "Trees", "Medium"),
    ("Validate Binary Search Tree", "Trees", "Medium"),
    ("Serialize and Deserialize Binary Tree", "Trees", "Hard"),
    ("Number of Islands", "Graphs", "Medium"),
    ("Clone Graph", "Graphs", "Medium"),
    ("Course Schedule", "Graphs", "Medium"),
    ("Rotting Oranges", "Graphs", "Medium"),
    ("Word Ladder", "Graphs", "Hard"),
    ("Flood Fill", "Graphs", "Easy"),
    ("Implement Queue Using Stacks", "Stack & Queue", "Easy"),
    ("Daily Temperatures", "Stack & Queue", "Medium"),
    ("Largest Rectangle in Histogram", "Stack & Queue", "Hard"),
    ("Top K Frequent Elements", "Hashing", "Medium"),
    ("Longest Consecutive Sequence", "Hashing", "Medium"),
]


def generate_problems(count: int = 50) -> list:
    """Generate a reproducible set of sample DSA problems."""

    if count <= 0:
        raise ValueError("Count must be greater than zero.")

    if count > len(PROBLEM_BANK):
        count = len(PROBLEM_BANK)

    random.seed(42)

    selected = random.sample(
        PROBLEM_BANK,
        count,
    )

    today = date.today()

    problems = []

    for index, (title, topic, difficulty) in enumerate(
        selected,
        start=1,
    ):
        status = random.choices(
            ["Solved", "Attempted", "Unsolved"],
            weights=[70, 20, 10],
            k=1,
        )[0]

        platform = random.choice(
            ["LeetCode", "GeeksForGeeks", "CodeChef"]
        )

        date_solved = None

        if status == "Solved":
            days_ago = random.randint(0, 45)
            date_solved = (
                today - timedelta(days=days_ago)
            ).isoformat()

        problems.append(
            {
                "title": title,
                "topic": topic,
                "difficulty": difficulty,
                "platform": platform,
                "status": status,
                "date_solved": date_solved,
            }
        )

    # Keep the demo data useful for analytics and revision scheduling.
    # Hashing intentionally has fewer than two solved problems so that
    # the weak-topic analysis has a visible result.
    hashing_items = [
        item for item in problems if item["topic"] == "Hashing"
    ]
    for index, item in enumerate(hashing_items):
        if index > 0:
            item["status"] = "Attempted"
            item["date_solved"] = None

    solved_items = [
        item for item in problems if item["status"] == "Solved"
    ]

    if solved_items:
        solved_items[0]["date_solved"] = today.isoformat()

    if len(solved_items) > 1:
        solved_items[1]["date_solved"] = (
            today - timedelta(days=1)
        ).isoformat()

    return problems


def save_problems(problems: list) -> None:
    """Save generated problems as formatted JSON."""

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            problems,
            file,
            indent=4,
        )


def main() -> None:
    """Generate and save sample DSA problems."""

    problems = generate_problems(50)
    save_problems(problems)

    print(
        f"Generated {len(problems)} sample problems."
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()