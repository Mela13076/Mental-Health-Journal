import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

def load(app):
    

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



