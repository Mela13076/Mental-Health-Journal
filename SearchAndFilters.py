import tkinter as tk
from tkinter import ttk
import json
from tkcalendar import DateEntry
from datetime import datetime
from collections import defaultdict
import re

def load(app, mood_var, thoughts_text):
    global search_field, mood_input, thoughts_input

    mood_input = mood_var
    thoughts_input = thoughts_text
    
    search_and_filter_entries_frame = tk.LabelFrame(app, text="Search and Filter Entries")
    search_and_filter_frame = tk.Frame(search_and_filter_entries_frame, borderwidth=2, relief="groove")

    search_label = tk.Label(search_and_filter_frame, text="Search Entries:")
    search_field = tk.Text(search_and_filter_frame, height=1, width=30)
    search_field.bind("<KeyRelease>", lambda e: filter_entries())

    filter_label = tk.Label(search_and_filter_frame, text="Filter Entires:")
    filter_frame = tk.Frame(search_and_filter_frame, borderwidth=2, relief="groove")

    left_frame = tk.Frame(filter_frame, borderwidth=2, relief="groove")
    left_frame.grid(row=0, column=0, padx=5, pady=5)
    right_frame = tk.Frame(filter_frame, borderwidth=2, relief="groove")
    right_frame.grid(row=0, column=1, padx=5, pady=5)

    add_mood_types(left_frame)
    add_keywords(right_frame)
    add_date(right_frame)
    add_filter_clear_btn(filter_frame)
    add_entries(search_and_filter_entries_frame)

    search_and_filter_entries_frame.grid(row=0, columnspan=3, padx=10, pady=5)
    search_and_filter_frame.pack(side='left', padx=10, pady=5)
    search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    search_field.grid(row=0, column=1, padx=10, pady=5)
    filter_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    filter_frame.grid(row=1, column=1, padx=10, pady=5)

def add_entries(search_and_filter_entries_frame):
    global entries_frame
    entries_frame = tk.Frame(search_and_filter_entries_frame, borderwidth=2)
    display_entries(load_entries(), entries_frame)
    entries_frame.pack(side='right', padx=10, pady=5)

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
    global keywords_map
    keywords_map = defaultdict(list)
    keywords_map['Happy'].extend(['Cheerful', 'Joy', 'Happy', 'Delight', 'Tearful', 'glad'])
    keywords_map['Sad'].extend(['Hopeless', 'Depressed', 'Concerned', 'Miserable', 'Heartbroken', 'Sad'])
    keywords_map['Anxious'].extend(['Fear', 'Anxious', 'Worry', 'Stress', 'Panic', 'Discomfort'])
    keywords_map['Neutral'].extend(['Disinterested', 'Undecided', 'Neutral', 'Unbiased', 'Uninvolved', 'Fair-minded'])

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

    global checked_keywords, keywords
    checked_keywords = {}
    keywords = sum(list(keywords_map.values()), [])
    for keyword in keywords:
        hashtag_keyword = '#'+keyword
        checked_keywords[hashtag_keyword] = tk.IntVar()
        tk.Checkbutton(keyword_inner_frame, text=hashtag_keyword, variable=checked_keywords[hashtag_keyword], command=filter_entries).pack(side="left")

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

def add_filter_clear_btn(filter_frame):
    clear_filters_btn = tk.Button(filter_frame, text="Clear all Filters", command=clear_filters)
    clear_filters_btn.grid(row=1, columnspan=2, padx=10, pady=10)

def clear_filters():
    selected_mood.set('')
    from_date_calendar.delete(0, 'end')
    to_date_calendar.delete(0, 'end')
    for keyword in keywords:
        hashtag_keyword = '#'+keyword
        if(checked_keywords[hashtag_keyword].get() == 1): checked_keywords[hashtag_keyword].set(0)
    filter_entries()

def filter_entries():
    thought_input = search_field.get("1.0", "end-1c")
    selected_mood_type = selected_mood.get()
    selected_from_date = from_date_calendar.get()
    selected_to_date = to_date_calendar.get()

    filtered__mood = list(filter(lambda entry: selected_mood_type in entry['Mood'], load_entries()))
    filtered_mood_date = list(filter(lambda filtered_entry: filter_by_date(filtered_entry['Date'].split(' ')[0], 
                                                selected_from_date, selected_to_date), filtered__mood))
    filtered_mood_date_keywords = filter_by_keywords(filtered_mood_date)
    filtered_mood_date_keywords_thaughts = filter_by_taughts(thought_input, filtered_mood_date_keywords)
    display_entries(filtered_mood_date_keywords_thaughts, entries_frame)

def filter_by_date(date, from_date, to_date):
    if from_date != '' and to_date != '':
        date = datetime.strptime(date, "%Y-%m-%d")
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        return from_date <= date <= to_date
    else: return True

def filter_by_keywords(filtered_mood_date):
    checked_keys = set()
    for key, values in keywords_map.items():
        for keyword in values:
            if(checked_keywords['#'+keyword].get() == 1):
                checked_keys.add(key)
    checked_keys = list(checked_keys)
    filtered_mood_date_keywords = []
    for checked_word in checked_keys:
        filtered_mood_date_keywords.extend(list(filter(lambda entry: checked_word.lower() == entry['Mood'].lower(), filtered_mood_date)))
    return filtered_mood_date_keywords if(len(checked_keys) > 0) else filtered_mood_date

def filter_by_taughts(thought_input, filtered_mood_date_keywords):
    words = list(filter(lambda word: word.lower()!='', re.split(r'\s+', thought_input))) if(len(thought_input) > 0) else ['']
    thoughts_len_map = defaultdict(list)
    for thought_entry in filtered_mood_date_keywords:
        size = len(list(filter(lambda word: word.lower() in thought_entry['Thoughts'].lower(), words)))
        if(size > 0):
            thoughts_len_map[size].append(thought_entry)
    return sum(list(dict(sorted(thoughts_len_map.items(), key = lambda item: item[0], reverse=True)).values()), [])

def display_entries(filtered_entries, entries_frame):
    treeview = ttk.Treeview(entries_frame, show="headings", columns=("Date", "Mood", "Thoughts"))
    treeview.grid(row=0, column=0)
    treeview.column("#1", width=120)
    treeview.heading("#1", text="Date")
    treeview.column("#2", width=100)
    treeview.heading("#2", text="Mood")
    treeview.column("#3", width=500)
    treeview.heading("#3", text="Thoughts")

    for filtered_entry in filtered_entries:
        treeview.insert("", "end", values=(filtered_entry["Date"], filtered_entry["Mood"], filtered_entry["Thoughts"]))

    treeview.bind("<Double-1>", lambda e: onDoubleClick(treeview))

def onDoubleClick(treeview):
    entry = list(treeview.item(treeview.selection()[0], "values"))

    mood_input.set(entry[1])
    thoughts_input.delete("1.0", "end")
    thoughts_input.insert(tk.END, entry[2])

def load_entries():
    try:
        with open("data.json") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        print("Unable to load data, file not found")
