import tkinter as tk
from tkinter import ttk
import json
from tkcalendar import DateEntry
from datetime import datetime
from collections import defaultdict
import re

def load(app, mood_var, thoughts_text):
    global root, search_field, mood_input, thoughts_input

    mood_input = mood_var
    thoughts_input = thoughts_text

    root = app
    search_label = tk.Label(app, text="Search Entries:")
    search_field = tk.Text(app, height=1, width=30)
    search_field.bind("<KeyRelease>", lambda e: filter_entries())
    #search_field.bind("<FocusIn>", lambda e: filter_entries())

    filter_label = tk.Label(app, text="Filter Entires:")
    filter_frame = tk.Frame(app, borderwidth=2, relief="groove")

    left_frame = tk.Frame(filter_frame, borderwidth=2, relief="groove")
    left_frame.grid(row=0, column=0, padx=5, pady=5)
    right_frame = tk.Frame(filter_frame, borderwidth=2, relief="groove")
    right_frame.grid(row=0, column=1, padx=5, pady=5)

    add_mood_types(left_frame)
    add_keywords(right_frame)
    add_date(right_frame)

    search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    search_field.grid(row=0, column=1, padx=10, pady=5)
    filter_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    filter_frame.grid(row=1, column=1, padx=10, pady=5)

def add_mood_types(left_frame):
    canvas = tk.Canvas(left_frame, width=100, height=110)

    scroll_bar = tk.Scrollbar(left_frame, orient='vertical', command=canvas.yview)

    canvas.configure(yscrollcommand=scroll_bar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    mood_type_inner_frame = tk.Frame(canvas)
    canvas.pack(side="left", fill="both", expand=1)
    scroll_bar.pack(side="right", fill="y")
    canvas.create_window((0, 0), window=mood_type_inner_frame, anchor="nw")
    
    global selected_mood
    selected_mood = tk.StringVar()
    for moodType in set(map(lambda entry: entry['Mood'], load_entries())):
        tk.Radiobutton(mood_type_inner_frame, text=moodType, variable=selected_mood, value=moodType, command=filter_entries).pack()

def add_keywords(right_frame):
    keyWords = ["#Cheerful", "#Joy", "#Happy", "#Delight", "#Tearful", "#Depression", "#Concerned"]

    keyword_outer_frame = tk.Frame(right_frame, borderwidth=2, relief="groove")
    keyword_outer_frame.pack()

    canvas = tk.Canvas(keyword_outer_frame, width=200, height=25)

    scroll_bar = tk.Scrollbar(keyword_outer_frame, orient='horizontal', command=canvas.xview)

    canvas.configure(xscrollcommand=scroll_bar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    keyword_inner_frame = tk.Frame(canvas)
    canvas.pack(fill="both", expand=True)
    scroll_bar.pack(side="bottom", fill="x")
    canvas.create_window((0, 0), window=keyword_inner_frame, anchor="nw")

    selected_keyword = {}
    for keyword in keyWords:
        selected_keyword[keyword] = tk.StringVar()
        tk.Checkbutton(keyword_inner_frame, text=keyword, variable=selected_keyword[keyword]).pack(side="left")
    

def add_date(right_frame):
    date_outer_frame = tk.Frame(right_frame, borderwidth=2, relief="groove")
    date_outer_frame.pack()

    from_date = tk.Label(date_outer_frame, text="Date from: ")
    from_date.grid(row=0, column=0)
    global from_date_calendar
    from_date_calendar = DateEntry(date_outer_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    from_date_calendar.delete(0, 'end')
    from_date_calendar.bind('<<DateEntrySelected>>', lambda e: filter_entries())
    from_date_calendar.grid(row=0, column=1)

    to_date = tk.Label(date_outer_frame, text="Date to: ")
    to_date.grid(row=1, column=0)
    global to_date_calendar
    to_date_calendar = DateEntry(date_outer_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    to_date_calendar.delete(0, 'end')
    to_date_calendar.bind('<<DateEntrySelected>>', lambda e: filter_entries())
    to_date_calendar.grid(row=1, column=1)

def filter_entries():
    thought_input = search_field.get("1.0", "end-1c")
    selected_mood_type = selected_mood.get()
    selected_from_date = from_date_calendar.get()
    selected_to_date = to_date_calendar.get()

    filtered__mood = list(filter(lambda entry: selected_mood_type in entry['Mood'], load_entries()))
    filtered_mood_date = list(filter(lambda filtered_entry: filter_by_date(filtered_entry['Date'].split(' ')[0], 
                                                selected_from_date, selected_to_date), filtered__mood))
    filtered_mood_date_thaughts = filter_by_taughts(thought_input, filtered_mood_date)
    search_popup(filtered_mood_date_thaughts)

def filter_by_date(date, from_date, to_date):
    if from_date != '' and to_date != '':
        date = datetime.strptime(date, "%Y-%m-%d")
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        return from_date <= date <= to_date
    else: return True

def filter_by_taughts(thought_input, thought_entries):
    words = list(filter(lambda word: word.lower()!='', re.split(r'\s+', thought_input))) if(len(thought_input) > 0) else ['']
    thoughts_len_map = defaultdict(list)
    for thought_entry in thought_entries:
        size = len(list(filter(lambda word: word.lower() in thought_entry['Thoughts'].lower(), words)))
        if(size > 0):
            thoughts_len_map[size].append(thought_entry)
    return sum(list(dict(sorted(thoughts_len_map.items(), key = lambda item: item[0], reverse=True)).values()), [])

def search_popup(filtered_entries):
    global pop_up
    if pop_up is None or not pop_up.winfo_exists():
        pop_up = tk.Toplevel(root)
    
    treeview = ttk.Treeview(pop_up, show="headings", columns=("Date", "Mood", "Thoughts"))
    treeview.grid(row=6, column=0, columnspan=5, padx=10, pady=10)
    treeview.heading("#1", text="Date")
    treeview.heading("#2", text="Mood")
    treeview.heading("#3", text="Thoughts")

    for filtered_entry in filtered_entries:
        treeview.insert("", "end", values=(filtered_entry["Date"], filtered_entry["Mood"], filtered_entry["Thoughts"]))

    treeview.bind("<Double-1>", lambda e: onDoubleClick(treeview, pop_up))

def onDoubleClick(treeview, pop_up):
    item = treeview.selection()[0]
    entry = list(treeview.item(item, "values"))

    mood_input.set(entry[1])
    thoughts_input.delete("1.0", "end")
    thoughts_input.insert(tk.END, entry[2])

    pop_up.destroy()
    pop_up = None

def load_entries():
    try:
        with open("data.json") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        print("Unable to load data, file not found")

pop_up = None
