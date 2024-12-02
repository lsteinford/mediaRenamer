#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import *
from functions import parse_folder, update_example, insert_preview, rename_file

window = tk.Tk()
window.title("Media Renamer")

frame = tk.Frame(window)
frame.pack()

# Notebook Attempt
notebook = ttk.Notebook(frame)
notebook.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

series_tab = ttk.Frame(frame)
notebook.add(series_tab, text="Series")

movie_tab = ttk.Frame(frame)
notebook.add(movie_tab, text="Movies")

widgets = {
    "series": {},
    "movies": {}
}

def create_combobox(frame, label_text, label_row, label_col, tab_name, widget_name, widget_row, widget_col, values):
    combobox = tk.Label(frame, text=label_text)
    combobox.grid(row=label_row, column=label_col)
    widgets[tab_name][widget_name] = ttk.Combobox(frame, values=values)
    widgets[tab_name][widget_name].grid(row=widget_row, column=widget_col)

def delim_options(frame, tab_name):
    create_combobox(frame, "Name Delim", 2, 0, tab_name, "name_delim", 3, 0, ['_',' ','-','.'])
    create_combobox(frame, "Info Delim", 2, 1, tab_name, "info_delim", 3, 1, ['-',' ','_','.'])
    create_combobox(frame, "Sub Delim", 2, 2, tab_name, "sub_delim", 3, 2, ['-',' ','_','.'])

    widgets[tab_name]["name_delim"].current(0)
    widgets[tab_name]["info_delim"].current(0)
    widgets[tab_name]["sub_delim"].current(0)

    widgets[tab_name]["lowercase"] = IntVar()
    lowercase_label = tk.Label(frame, text="Case Sensitivity")
    lowercase_label.grid(row=4, column=0, columnspan=2)
    lowercase_check = tk.Checkbutton(frame, variable=widgets[tab_name]["lowercase"], onvalue=1, offvalue=0, text="Lowercase Names")
    lowercase_check.grid(row=5, column=0, columnspan=2)

def build_series_tab(frame):
    delim_options(frame, "series")

    widgets["series"]["episode"] = IntVar()
    episode_name_label = tk.Label(frame, text="Episode Names")
    episode_name_label.grid(row=4, column=1, columnspan=2)
    episode_name_check = tk.Checkbutton(frame, variable=widgets["series"]["episode"], onvalue=1, offvalue=0, text="Episode names in file name")
    episode_name_check.grid(row=5, column=1, columnspan=2)

def build_movie_tab(frame):    
    delim_options(frame, "movies")

def get_selected_tab():
    return notebook.tab(notebook.select(), "text").lower()

def get_media_type():
    selected_tab = get_selected_tab()
    return 1 if selected_tab == "series" else 0

build_movie_tab(movie_tab)
build_series_tab(series_tab)

def tab_change(event):
    selected_tab = notebook.tab(notebook.select(), "text").lower()
    media_type = 1 if selected_tab == "series" else 0
    update_example(
        widgets[selected_tab]["name_delim"],
        widgets[selected_tab]["info_delim"],
        widgets[selected_tab]["sub_delim"],
        example_text,
        media_type,
        widgets[selected_tab].get("episode", None),  # Handle missing "episode" key gracefully
        widgets[selected_tab]["lowercase"]
    )

notebook.bind("<<NotebookTabChanged>>", tab_change)

for widget in series_tab.winfo_children():
    widget.grid_configure(padx=10, pady=5)

for widget in movie_tab.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Example Convention Section
naming_conv_frame = tk.LabelFrame(frame, text="Naming Convention Example")
naming_conv_frame.grid(row=1,column=0, columnspan=2, padx=20, pady=20)

example_text = tk.Text(naming_conv_frame, height=1, width=45)
example_text.grid(row=0, column=0, columnspan=3)

for widget in naming_conv_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Folder Selection
show_info_frame = tk.LabelFrame(frame, text="Folder Information")
show_info_frame.grid(row=2, column=0, columnspan=2, padx=150, pady=20, sticky='nsew')

folder_name_label = tk.Label(show_info_frame, text="Show Folder")
folder_name_label.grid(row=0, column=0)

folder_name_entry = tk.Entry(show_info_frame, width=50)
folder_name_entry.grid(row=1, column=0, columnspan=2)

folder_button = tk.Button(show_info_frame, text="Check Folder", command=lambda: parse_folder(folder_name_entry,
                                                                                             folder_list))
folder_button.grid(row=1, column=2)

preview_button = tk.Button(show_info_frame, text="Preview", command=lambda: insert_preview(folder_name_entry,
                                                                                           preview_list,
                                                                                           widgets[get_selected_tab()]["name_delim"],
                                                                                           widgets[get_selected_tab()]["info_delim"],
                                                                                           widgets[get_selected_tab()]["sub_delim"],
                                                                                           get_media_type(),
                                                                                           widgets[get_selected_tab()].get("episode", None),
                                                                                           widgets[get_selected_tab()]["lowercase"]))
preview_button.grid(row=2, column=0, columnspan=2)

rename_button = tk.Button(show_info_frame, text="Rename", command=lambda: rename_file(folder_name_entry,
                                                                                      widgets[get_selected_tab()]["name_delim"],
                                                                                      widgets[get_selected_tab()]["info_delim"],
                                                                                      get_media_type(),
                                                                                      widgets[get_selected_tab()].get("episode", None),
                                                                                      widgets[get_selected_tab()]["lowercase"]))
rename_button.grid(row=2, column=1, columnspan=2)

for widget in show_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Folder View
folder_label = tk.LabelFrame(frame, text="Folder View")
folder_label.grid(row=3, column=0, padx=20, pady=20)

preview_label = tk.LabelFrame(frame, text="File Preview")
preview_label.grid(row=3, column=1, padx=20, pady=20)

folder_list = Listbox(folder_label, selectbackground='white', highlightcolor='blue', width=50)
preview_list = Listbox(preview_label, selectbackground='white', highlightcolor='blue', width=50)

for widget in folder_label.winfo_children():
    widget.grid_configure(padx=10, pady=10)

for widget in preview_label.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Binding and Function Calls

def bind_tab_widgets(tab_name):

    if tab_name == "series":
        episode = widgets[tab_name]["episode"]
        episode.trace_add("write", lambda *args:update_example(name_delim, info_delim, sub_delim,
                                                               example_text, get_media_type(),
                                                               episode, lowercase))

    name_delim = widgets[tab_name]["name_delim"]
    info_delim = widgets[tab_name]["info_delim"]
    sub_delim = widgets[tab_name]["sub_delim"]
    lowercase = widgets[tab_name]["lowercase"]
    

    name_delim.bind("<<ComboboxSelected>>", lambda event: update_example(name_delim, info_delim, sub_delim,
                                                                         example_text, get_media_type(),
                                                                         widgets[get_selected_tab()].get("episode", None), lowercase))
    info_delim.bind("<<ComboboxSelected>>", lambda event: update_example(name_delim, info_delim, sub_delim,
                                                                         example_text, get_media_type(),
                                                                         widgets[get_selected_tab()].get("episode", None), lowercase))
    sub_delim.bind("<<ComboboxSelected>>", lambda event: update_example(name_delim, info_delim, sub_delim,
                                                                        example_text, get_media_type(),
                                                                        widgets[get_selected_tab()].get("episode", None), lowercase))
    
    lowercase.trace_add("write", lambda *args:update_example(name_delim, info_delim, sub_delim,
                                                             example_text, get_media_type(),
                                                             widgets[get_selected_tab()].get("episode", None), lowercase))

bind_tab_widgets("series")
bind_tab_widgets("movies")

update_example(
    widgets["series"]["name_delim"], 
    widgets["series"]["info_delim"], 
    widgets["series"]["sub_delim"], 
    example_text, 
    get_media_type(), 
    widgets["series"].get("episode", None), 
    widgets["series"]["lowercase"])


