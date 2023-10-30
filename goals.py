import json
import tkinter as tk
import os

# Initialize goals as an empty list
goals = []

def load_goals():
    global goals
    if os.path.exists("goals.json"):
        with open("goals.json", "r") as file:
            try:
                goals = json.load(file)
            except json.JSONDecodeError:
                # If the file is not valid JSON, initialize goals as an empty list
                goals = []

def add_goal(goal_entry, goal_listbox):
    goal = goal_entry.get()
    if goal:
        goals.append({"Goal": goal, "Completed": False})
        goal_listbox.insert(tk.END, goal)
        goal_entry.delete(0, tk.END)
        save_goals_to_json()

def mark_completed(goal_listbox):
    selected_goal = goal_listbox.get(tk.ACTIVE)
    if selected_goal:
        for goal in goals:
            if goal["Goal"] == selected_goal:
                goal["Completed"] = True
                goal_listbox.itemconfig(tk.ACTIVE, {'bg': 'light green'})
        save_goals_to_json()
        remove_completed_goals(goal_listbox)

def save_goals_to_json():
    with open("goals.json", "w") as file:
        json.dump(goals, file, indent=4)

def remove_completed_goals(goal_listbox):
    global goals
    goals = [goal for goal in goals if not goal["Completed"]]
    save_goals_to_json()

def populate_goals(goal_listbox):
    for goal in goals:
        goal_text = goal["Goal"]
        goal_listbox.insert(tk.END, goal_text)

# Load goals at the beginning
load_goals()

#this is the final code