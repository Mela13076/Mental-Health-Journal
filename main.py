import tkinter as tk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
import json

# Function to save journal entries to JSON file (existing code)
def save_entry():
    entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mood = mood_var.get()
    thoughts = thoughts_text.get("1.0", "end-1c")

    # Read existing data from JSON file
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Add the new entry to the data
    data.append({
        "Date": entry_date,
        "Mood": mood,
        "Thoughts": thoughts
    })

    # Write the updated data back to the JSON file
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    clear_fields()

# Function to clear input fields (existing code)
def clear_fields():
    mood_var.set("")
    thoughts_text.delete("1.0", "end")

# Function to add a goal to the list
def add_goal():
    goal = goal_entry.get()
    if goal:
        goals.append({"Goal": goal, "Completed": False})
        goal_listbox.insert(tk.END, goal)
        goal_entry.delete(0, tk.END)

# Function to mark a goal as completed
def mark_completed():
    selected_goal = goal_listbox.get(tk.ACTIVE)
    if selected_goal:
        for goal in goals:
            if goal["Goal"] == selected_goal:
                goal["Completed"] = True
                goal_listbox.itemconfig(tk.ACTIVE, {'bg': 'light green'})

# Function to view goals
def view_goals():
    view_window = tk.Toplevel(app)
    view_window.title("Goals List")

    for goal in goals:
        goal_text = goal["Goal"]
        completed = " (Completed)" if goal["Completed"] else ""
        goal_label = tk.Label(view_window, text=goal_text + completed)
        goal_label.pack()

# Function to toggle the visibility of the goals list
def toggle_goals_visibility():
    if goal_listbox.winfo_viewable():
        goal_listbox.grid_remove()
        toggle_visibility_button.config(text="Show Goals")
    else:
        goal_listbox.grid()
        toggle_visibility_button.config(text="Hide Goals")

# Create the main application window
app = tk.Tk()
app.title("Mental Health Journal")

# Create and configure frames
journal_frame = ttk.LabelFrame(app, text="Journal Entry")
analytics_frame = ttk.LabelFrame(app, text="Mood Analytics")
goals_frame = ttk.LabelFrame(app, text="Self-Improvement Goals")

journal_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
analytics_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
goals_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

# Journal Entry Widgets (existing code)
mood_label = tk.Label(journal_frame, text="Mood:")
mood_var = tk.StringVar()
mood_entry = ttk.Combobox(journal_frame, textvariable=mood_var, values=["Happy", "Sad", "Anxious", "Neutral", "Other"])
thoughts_label = tk.Label(journal_frame, text="Thoughts/Feelings:")
thoughts_text = tk.Text(journal_frame, height=10, width=30)
save_button = tk.Button(journal_frame, text="Save Entry", command=save_entry)
clear_button = tk.Button(journal_frame, text="Clear Fields", command=clear_fields)

# Mood Analytics Widgets (existing code)
def show_mood_analytics_barchart():
    # Read mood data from the JSON file
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Initialize a dictionary to store mood counts
    mood_counts = {"Happy": 0, "Sad": 0, "Neutral": 0, "Anxious": 0, "Other": 0}

    # Count the occurrences of each mood in the data
    for entry in data:
        mood = entry.get("Mood", "")
        if mood in mood_counts:
            mood_counts[mood] += 1

    # Extract mood labels and counts from the dictionary
    moods = list(mood_counts.keys())
    counts = list(mood_counts.values())

    # Create a bar chart
    plt.bar(moods, counts)
    plt.xlabel("Mood")
    plt.ylabel("Count")
    plt.title("Mood Analytics")
    plt.show()

show_bar_chart_button = tk.Button(analytics_frame, text="Show Mood Bar Chart", command=show_mood_analytics_barchart)

def show_mood_analytics_piechart():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Initialize a dictionary to store mood counts
    mood_counts = {"Happy": 0, "Sad": 0, "Neutral": 0, "Anxious": 0, "Other": 0}

    # Count the occurrences of each mood in the data
    for entry in data:
        mood = entry.get("Mood", "")
        if mood in mood_counts:
            mood_counts[mood] += 1

    # Extract mood labels and counts from the dictionary
    moods = list(mood_counts.keys())
    counts = list(mood_counts.values())

    fig, ax = plt.subplots()
    ax.pie(counts, labels=moods, autopct='%1.1f%%')
    plt.show()

show_pie_chart_button = tk.Button(analytics_frame, text="Show Mood Pie Chart", command=show_mood_analytics_piechart)

# Self-Improvement Goals Widgets
goal_listbox = tk.Listbox(goals_frame, height=10, width=40)
goal_entry = tk.Entry(goals_frame)
add_goal_button = tk.Button(goals_frame, text="Add Goal", command=add_goal)
mark_completed_button = tk.Button(goals_frame, text="Mark Completed", command=mark_completed)
view_goals_button = tk.Button(goals_frame, text="View Goals", command=view_goals)
toggle_visibility_button = tk.Button(goals_frame, text="Toggle Visibility", command=toggle_goals_visibility)

# Grid layout for widgets in Journal Entry frame (existing code)
mood_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
mood_entry.grid(row=0, column=1, padx=10, pady=5)
thoughts_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
thoughts_text.grid(row=1, column=1, padx=10, pady=5, rowspan=3)
save_button.grid(row=4, column=0, padx=10, pady=10)
clear_button.grid(row=4, column=1, padx=10, pady=10)

# Grid layout for widgets in Mood Analytics frame (existing code)
show_bar_chart_button.grid(row=0, column=0, padx=10, pady=10)
show_pie_chart_button.grid(row=2, column=0, padx=10, pady=10)

# Grid layout for widgets in Self-Improvement Goals frame
goal_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=5, columnspan=2)
goal_entry.grid(row=6, column=0, padx=10, pady=5)
add_goal_button.grid(row=6, column=1, padx=10, pady=5)
mark_completed_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
view_goals_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
toggle_visibility_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# Initialize goals list
goals = []

# Start the Tkinter main loop
app.mainloop()
