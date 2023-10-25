import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

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

# Function to view goals
def view_goals():
    view_window = tk.Toplevel(app)
    view_window.title("Goals List")

    # Create a text widget to display the goals with a larger font
    goals_text = tk.Text(view_window, height=15, width=40, wrap=tk.WORD, font=("Helvetica", 12))
    goals_text.pack()

    for goal in goals:
        goal_text = goal["Goal"]
        completed = " (Completed)" if goal["Completed"] else ""
        goal_text = goal_text + completed

        # Insert the goal text with a slightly larger font size
        goals_text.insert(tk.END, goal_text + "\n")

# Function to save goals to a JSON file
def save_goals_to_json():
    with open("goals.json", "w") as file:
        json.dump(goals, file, indent=4)

# Function to load goals from a JSON file
def load_goals_from_json():
    try:
        with open("goals.json", "r") as file:
            loaded_goals = json.load(file)
            goals.clear()
            for goal in loaded_goals:
                goals.append(goal)
    except FileNotFoundError:
        goals.clear()

# Function to add a goal to the list
def add_goal():
    goal = goal_entry.get()
    if goal:
        goals.append({"Goal": goal, "Completed": False})
        goal_entry.delete(0, tk.END)
        save_goals_to_json()
        update_goals_listbox()

# Function to update the goals listbox
def update_goals_listbox():
    goal_listbox.delete(0, tk.END)
    for goal in goals:
        goal_text = goal["Goal"]
        goal_listbox.insert(tk.END, goal_text)

def toggle_self_improvement():
    global self_improvement_visible
    if self_improvement_visible:
        goals_frame.grid_remove()
    else:
        goals_frame.grid()
    self_improvement_visible = not self_improvement_visible

app = tk.Tk()
app.title("Mental Health Journal")

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
def show_mood_analytics():
    # Retrieve mood data from the journal (you may need to parse the journal file)
    # For simplicity, let's assume a static mood dataset
    moods = ["Happy", "Sad", "Neutral", "Anxious"]
    mood_counts = [12, 5, 8, 3]

    # Create a bar chart
    plt.bar(moods, mood_counts)
    plt.xlabel("Mood")
    plt.ylabel("Count")
    plt.title("Mood Analytics")
    plt.show()

show_analytics_button = tk.Button(analytics_frame, text="Show Mood Analytics", command=show_mood_analytics)

# Self-Improvement Goals Widgets
goal_listbox = tk.Listbox(goals_frame, height=10, width=40)
goal_entry = tk.Entry(goals_frame)
add_goal_button = tk.Button(goals_frame, text="Add Goal", command=add_goal)
view_goals_button = tk.Button(goals_frame, text="View Goals", command=view_goals)

mood_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
mood_entry.grid(row=0, column=1, padx=10, pady=5)
thoughts_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
thoughts_text.grid(row=1, column=1, padx=10, pady=5, rowspan=3)
save_button.grid(row=4, column=0, padx=10, pady=10)
clear_button.grid(row=4, column=1, padx=10, pady=10)

show_analytics_button.grid(row=0, column=0, padx=10, pady=10)

goal_entry.grid(row=6, column=0, padx=10, pady=5)
add_goal_button.grid(row=6, column=1, padx=10, pady=5)
view_goals_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Initialize goals list
goals = []
self_improvement_visible = False

self_improvement_button = tk.Button(app, text="Self Improvement Goals", command=toggle_self_improvement)
self_improvement_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

app.mainloop()
