import tkinter as tk
import json
from tkcalendar import DateEntry

def load(app):
    search_label = tk.Label(app, text="Search Entries:")
    search_field = tk.Text(app, height=1, width=30)

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
    
    selected_mood = tk.StringVar()
    for moodType in load_mood_types():
        tk.Radiobutton(mood_type_inner_frame, text=moodType, variable=selected_mood, value=moodType).pack()

def load_mood_types():
    try:
        with open("data.json") as jsonFile:
            entries = json.load(jsonFile)
        return set(map(lambda entry: entry['Mood'], entries))
    except FileNotFoundError:
        print("Unable to load data, file not found")

def add_keywords(right_frame):
    keyWords = ["#frame", "#key2", "#key3", "#key4", "#key5", "#key6", "#key7"]

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
    from_date_calendar = DateEntry(date_outer_frame, selectmode='day')
    from_date_calendar.grid(row=0, column=1)

    to_date = tk.Label(date_outer_frame, text="Date to: ")
    to_date.grid(row=1, column=0)
    to_date_calendar = DateEntry(date_outer_frame, selectmode='day')
    to_date_calendar.grid(row=1, column=1)
