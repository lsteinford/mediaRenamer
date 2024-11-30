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
notebook.add(movie_tab, text="Movie")

widgets = {
    "series": {},
    "movies": {}
}

def delim_options(frame, tab_name):
    name_delim = tk.Label(frame, text="Name Delim")
    name_delim.grid(row=2, column=0)
    widgets[tab_name]["name_delim"] = ttk.Combobox(frame, values=['_',' ','-','.'])
    widgets[tab_name]["name_delim"].grid(row=3, column=0)
    

    info_delim = tk.Label(frame, text="Info Delim")
    info_delim.grid(row=2, column=1)
    widgets[tab_name]["info_delim"] = ttk.Combobox(frame, values=['-',' ','_','.'])
    widgets[tab_name]["info_delim"].grid(row=3, column=1)
    

    sub_delim = tk.Label(frame, text="Sub-Title Delim")
    widgets[tab_name]["sub_delim"] = ttk.Combobox(frame, values=['-',' ','_','.'])
    sub_delim.grid(row=2, column=2)
    widgets[tab_name]["sub_delim"].grid(row=3, column=2)
    

    widgets[tab_name]["name_delim"].current(0)
    widgets[tab_name]["info_delim"].current(0)
    widgets[tab_name]["sub_delim"].current(0)

    widgets[tab_name]["lowercase"] = IntVar()
    lowercase_label = tk.Label(frame, text="Case Sensitivity")
    lowercase_check = tk.Checkbutton(frame, variable=widgets[tab_name]["lowercase"], onvalue=1, offvalue=0, text="Lowercase Names")
    lowercase_label.grid(row=4, column=0)
    lowercase_check.grid(row=5, column=0)

def build_series_tab(frame):
    delim_options(frame, "series")

    widgets["series"]["episode"] = IntVar()
    episode_name_label = tk.Label(frame, text="Episode Names")
    episode_name_label.grid(row=4, column=1)
    episode_name_check = tk.Checkbutton(frame, variable=widgets["series"]["episode"], onvalue=1, offvalue=0, text="Episode names in file name")
    episode_name_check.grid(row=5, column=1)

def build_movie_tab(frame):    
    delim_options(frame, "movies")

build_movie_tab(movie_tab)
build_series_tab(series_tab)

# Example Convention Section
naming_conv_frame = tk.LabelFrame(frame, text="Naming Convention Example")
naming_conv_frame.grid(row=1,column=0, columnspan=2, padx=20, pady=20)

example_text = tk.Text(naming_conv_frame, height=1, width=45)
example_text.grid(row=0, column=0, columnspan=3)

for widget in naming_conv_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Folder Selection
show_info_frame = tk.LabelFrame(frame, text="Folder Information")
show_info_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

folder_name_label = tk.Label(show_info_frame, text="Show Folder")
folder_name_label.grid(row=0, column=0)

folder_name_entry = tk.Entry(show_info_frame)
folder_name_entry.grid(row=1, column=0, columnspan=2, sticky='nsew')

folder_button = tk.Button(show_info_frame, text="Check Folder", command=lambda: parse_folder(folder_name_entry, folder_list))
folder_button.grid(row=1, column=2)

preview_button = tk.Button(show_info_frame, text="Preview", command=lambda: insert_preview(folder_name_entry, preview_list, name_delim_combobox, info_delim_combobox, sub_delim_combobox, mediaType, episode, lowercase))
preview_button.grid(row=2, column=0, columnspan=2)

rename_button = tk.Button(show_info_frame, text="Rename", command=lambda: rename_file(folder_name_entry, name_delim_combobox, info_delim_combobox, mediaType, episode, lowercase))
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
        episode.trace_add("write", lambda *args:update_example(name_delim, info_delim, sub_delim, example_text, notebook, episode, lowercase))
        
    name_delim = widgets[tab_name]["name_delim"]
    info_delim = widgets[tab_name]["info_delim"]
    sub_delim = widgets[tab_name]["sub_delim"]
    lowercase = widgets[tab_name]["lowercase"]
    

    name_delim.bind("<<ComboboxSelected>>", lambda event: update_example(name_delim, info_delim, sub_delim, example_text, notebook, episode, lowercase))
    info_delim.bind("<<ComboboxSelected>>", lambda event: update_example(name_delim, info_delim, sub_delim, example_text, notebook, episode, lowercase))
    sub_delim.bind("<<ComboboxSelected>>", lambda event: update_example(name_delim, info_delim, sub_delim, example_text, notebook, episode, lowercase))
    
    lowercase.trace_add("write", lambda *args:update_example(name_delim, info_delim, sub_delim, example_text, notebook, episode, lowercase))

bind_tab_widgets("series")
bind_tab_widgets("movies")

update_example(
    widgets["series"]["name_delim"], 
    widgets["series"]["info_delim"], 
    widgets["series"]["sub_delim"], 
    example_text, 
    notebook, 
    widgets["series"]["episode"], 
    widgets["series"]["lowercase"])


