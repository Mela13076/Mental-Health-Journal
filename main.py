import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

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

# Function to add a goal to the list and save to JSON file
def add_goal():
    goal = goal_entry.get()
    if goal:
        goals.append({"Goal": goal, "Completed": False})
        goal_listbox.insert(tk.END, goal)
        goal_entry.delete(0, tk.END)

        # Save the updated goals list to a JSON file
        save_goals_to_json()

# Function to mark a goal as completed and save to JSON file
def mark_completed():
    selected_goal = goal_listbox.get(tk.ACTIVE)
    if selected_goal:
        for goal in goals:
            if goal["Goal"] == selected_goal:
                goal["Completed"] = True
                goal_listbox.itemconfig(tk.ACTIVE, {'bg': 'light green'})
        
        # Save the updated goals list to a JSON file and remove completed goals
        save_goals_to_json()
        remove_completed_goals()

# Function to save goals to a JSON file
def save_goals_to_json():
    with open("goals.json", "w") as file:
        json.dump(goals, file, indent=4)

# Function to remove completed goals from the JSON file
def remove_completed_goals():
    goals[:] = [goal for goal in goals if not goal["Completed"]]
    save_goals_to_json()

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

# Function to show mood analytics (existing code)
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
mark_completed_button = tk.Button(goals_frame, text="Mark Completed", command=mark_completed)

# Grid layout for widgets in Journal Entry frame
mood_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
mood_entry.grid(row=0, column=1, padx=10, pady=5)
thoughts_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
thoughts_text.grid(row=1, column=1, padx=10, pady=5, rowspan=3)
save_button.grid(row=4, column=0, padx=10, pady=10)
clear_button.grid(row=4, column=1, padx=10, pady=10)

# Grid layout for widgets in Mood Analytics frame
show_analytics_button.grid(row=0, column=0, padx=10, pady=10)

# Grid layout for widgets in Self-Improvement Goals frame
goal_entry.grid(row=6, column=0, padx=10, pady=5)
add_goal_button.grid(row=6, column=1, padx=10, pady=5)
mark_completed_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
goal_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=5, columnspan=2)

# Initialize goals list and load from JSON file if it exists
goals = []

if os.path.exists("goals.json"):
    with open("goals.json", "r") as file:
        goals = json.load(file)

# Populate the goal_listbox with existing goals
for goal in goals:
    goal_text = goal["Goal"]
    goal_listbox.insert(tk.END, goal_text)

# Start the Tkinter main loop
app.mainloop()
