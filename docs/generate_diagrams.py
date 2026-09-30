import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def box(ax, x, y, w, h, text, fontsize=10):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.5,
        fill=False
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=fontsize
    )


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="->",
            mutation_scale=15,
            linewidth=1.2
        )
    )


# ---------------- ARCHITECTURE ----------------
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

ax.text(6, 7.5, "DSA Progress & Revision Analyzer - Architecture",
        ha="center", fontsize=16, fontweight="bold")

box(ax, 4.3, 6.1, 3.4, 0.7, "CLI Interface\nmain.py / __main__.py")
box(ax, 0.5, 4.5, 2.5, 0.8, "Problem Management\nmanager.py")
box(ax, 3.4, 4.5, 2.5, 0.8, "Analytics Engine\nanalytics.py")
box(ax, 6.1, 4.5, 2.5, 0.8, "Revision Scheduler\nscheduler.py")
box(ax, 9.0, 4.5, 2.5, 0.8, "Report Generator\nreporter.py")

box(ax, 4.3, 2.8, 3.4, 0.8, "Validation & Models\nvalidators.py + models.py")
box(ax, 4.3, 1.2, 3.4, 0.8, "SQLite Storage\nstorage.py")

arrow(ax, 6, 6.1, 1.75, 5.3)
arrow(ax, 6, 6.1, 4.65, 5.3)
arrow(ax, 6, 6.1, 7.35, 5.3)
arrow(ax, 6, 6.1, 10.25, 5.3)

arrow(ax, 1.75, 4.5, 5.5, 3.6)
arrow(ax, 4.65, 4.5, 5.8, 3.6)
arrow(ax, 7.35, 4.5, 6.2, 3.6)
arrow(ax, 10.25, 4.5, 6.5, 3.6)

arrow(ax, 6, 2.8, 6, 2.0)

fig.savefig("docs/architecture.png", dpi=200, bbox_inches="tight")
plt.close(fig)


# ---------------- USE CASE ----------------
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

ax.text(6, 7.5, "DSA Tracker - Use Case Diagram",
        ha="center", fontsize=16, fontweight="bold")

box(ax, 0.7, 3.0, 2.0, 1.0, "DSA Student", 12)
box(ax, 4.2, 5.8, 2.8, 0.7, "Add / Update Problems")
box(ax, 8.0, 5.8, 2.8, 0.7, "Search / Filter Problems")
box(ax, 4.2, 4.3, 2.8, 0.7, "View Analytics")
box(ax, 8.0, 4.3, 2.8, 0.7, "Check Due Revisions")
box(ax, 4.2, 2.8, 2.8, 0.7, "Record Revision")
box(ax, 8.0, 2.8, 2.8, 0.7, "Generate Reports")
box(ax, 4.2, 1.3, 2.8, 0.7, "View Revision History")
box(ax, 8.0, 1.3, 2.8, 0.7, "Import Sample Data")

for y in [6.15, 4.65, 3.15, 1.65]:
    arrow(ax, 2.7, 3.5, 4.2, y)

fig.savefig("docs/use_case.png", dpi=200, bbox_inches="tight")
plt.close(fig)


# ---------------- ER DIAGRAM ----------------
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

ax.text(
    6, 7.5,
    "DSA Tracker - ER Diagram",
    ha="center",
    fontsize=16,
    fontweight="bold"
)

# PROBLEMS entity
box(ax, 0.8, 3.4, 4.2, 2.8,
    "PROBLEMS\n\n"
    "PK  id\n"
    "title\n"
    "topic\n"
    "difficulty\n"
    "platform\n"
    "status\n"
    "solved_date",
    fontsize=11
)

# REVISION_LOG entity
box(ax, 7.0, 3.4, 4.2, 2.8,
    "REVISION_LOG\n\n"
    "PK  id\n"
    "FK  problem_id\n"
    "revision_date\n"
    "rating\n"
    "next_revision",
    fontsize=11
)

# Relationship
arrow(ax, 5.0, 4.8, 7.0, 4.8)

ax.text(
    6, 5.15,
    "1 : N",
    ha="center",
    fontsize=12,
    fontweight="bold"
)

fig.savefig(
    "docs/er_diagram.png",
    dpi=200,
    bbox_inches="tight"
)
plt.close(fig)


# ---------------- REVISION WORKFLOW ----------------
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis("off")

ax.text(6, 8.5, "Spaced Repetition Revision Workflow",
        ha="center", fontsize=16, fontweight="bold")

box(ax, 4.3, 7.0, 3.4, 0.7, "Problem Solved")
box(ax, 4.3, 5.6, 3.4, 0.7, "Revision Becomes Due")
box(ax, 1.0, 4.0, 2.8, 0.7, "Again\n1 day")
box(ax, 4.6, 4.0, 2.8, 0.7, "Hard\n3 days")
box(ax, 8.2, 4.0, 2.8, 0.7, "Good / Easy\n7+ days")
box(ax, 4.3, 2.4, 3.4, 0.7, "Schedule Next Revision")
box(ax, 4.3, 0.9, 3.4, 0.7, "Revision History Stored")

arrow(ax, 6, 7.0, 6, 6.3)
arrow(ax, 6, 5.6, 2.4, 4.7)
arrow(ax, 6, 5.6, 6, 4.7)
arrow(ax, 6, 5.6, 9.6, 4.7)
arrow(ax, 2.4, 4.0, 5.2, 3.1)
arrow(ax, 6, 4.0, 6, 3.1)
arrow(ax, 9.6, 4.0, 6.8, 3.1)
arrow(ax, 6, 2.4, 6, 1.6)

fig.savefig("docs/revision_workflow.png", dpi=200, bbox_inches="tight")
plt.close(fig)

print("Generated 4 design diagrams successfully.")
