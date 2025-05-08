import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

# Start date of the project
start_date = datetime(2025, 5, 1)

# Task assignments with (assignee, task name, duration in days) in waterfall order
ordered_tasks = [
    ("David", "Literature review", 5),
    ("Dan", "Finalize system requirements", 5),
    ("Dongwoo", "Obtain ethical approvals", 10),
    ("Dongwoo", "System architecture (pipeline & app design)", 10),
    ("David", "Develop occupancy detection algorithm", 10),
    ("Dan", "Build smartphone app prototype", 10),
    ("Dongwoo", "Data collection & model refinement", 10),
    ("Dongwoo", "System integration & deployment", 10),
    ("Dongwoo", "Pilot testing with initial users", 10),
    ("David", "Full-scale data collection", 7),
    ("Dongwoo", "Statistical analysis of results", 7),
    ("Dan", "System refinement", 8),
    ("Dan", "Report writing & publications", 8)
]

# Define a unique color for each assignee
assignee_colors = {
    "David": "#1f77b4",   # blue
    "Dan": "#ff7f0e",     # orange
    "Dongwoo": "#2ca02c"  # green
}

# Prepare lists for plotting
task_names = []
start_dates = []
durations = []
task_colors = []
task_assignees = []

current_date = start_date

# Fill in task data
for assignee, task_name, duration in ordered_tasks:
    task_names.append(task_name)
    start_dates.append(current_date)
    durations.append(duration)
    task_colors.append(assignee_colors[assignee])
    task_assignees.append(assignee)
    current_date += timedelta(days=duration)

# Plotting the Gantt chart
fig, ax = plt.subplots(figsize=(14, 9))
bars = ax.barh(task_names, durations, left=start_dates, color=task_colors, edgecolor='black')

# Add duration and assignee labels inside each bar
for bar, assignee in zip(bars, task_assignees):
    width = bar.get_width()
    start_x = bar.get_x()
    ax.text(start_x + width / 2, bar.get_y() + bar.get_height() / 2,
            f"{int(width)}d\n{assignee}", ha='center', va='center',
            fontsize=9, color='white', fontweight='bold')

# Axis labels and title
ax.set_xlabel('Timeline', fontsize=12, fontweight='bold')
ax.set_title('Project Gantt Chart Colored by Assignee (Waterfall Model)', fontsize=14, fontweight='bold')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# Rotate x-ticks and format
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Add legend
legend_patches = [mpatches.Patch(color=color, label=person) for person, color in assignee_colors.items()]
ax.legend(handles=legend_patches, title="Assignee", loc='upper right')

# Add gridlines and reverse y-axis for proper order
plt.grid(True, axis='x', linestyle='--', alpha=0.6)
plt.gca().invert_yaxis()

# Save chart as image
plt.savefig("gantt_chart_by_assignee.png")
plt.show()
