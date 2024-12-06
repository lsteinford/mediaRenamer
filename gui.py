#!/usr/bin/env python3
from tkinter import *
from tkinter import filedialog
import customtkinter as ctk
from functions import update_example, parse_folder, insert_preview, rename_file

# Set theme and color options
ctk.set_appearance_mode("system") # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue") # Themes: blue (default), dark-blue, green

root =ctk.CTk()

root.title("Media Renamer")

frame = ctk.CTkFrame(root)
frame.pack()

# Example Text Section
example_frame = ctk.CTkFrame(frame)
example_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

example_label = ctk.CTkLabel(example_frame, text="Naming Convention Example")
example_label.grid(row=0, column=0)

example_text = ctk.CTkTextbox(example_frame, height=1, width=400, state=DISABLED)
example_text.grid(row=1, column=0, columnspan=2)

for widget in example_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Create tabs
type_tab = ctk.CTkTabview(frame, command=lambda:update_example(widgets, example_text, get_selected_tab()))
type_tab.grid(row=0, column=0, columnspan=2)

series_tab = type_tab.add("Series")
movie_tab = type_tab.add("Movies")

widgets = {
    "series": {},
    "movies": {}
}

naming_convention = {
    "name_delim": {},
    "info_delim": {},
    "sub_delim": {},
    "lowercase": {},
    "episode": {}
}

# Create tab screens
def create_combobox(frame, label_text, label_row, label_col, tab_name, widget_name, widget_row, widget_col, values):
    combobox = ctk.CTkLabel(frame, text=label_text)
    combobox.grid(row=label_row, column=label_col)
    widgets[tab_name][widget_name] = ctk.CTkComboBox(frame, values=values, command=lambda _:update_example(widgets, example_text, get_selected_tab()))
    widgets[tab_name][widget_name].grid(row=widget_row, column=widget_col)

def format_options(frame, tab_name):
    create_combobox(frame, "Name Delim", 2, 0, tab_name, "name_delim", 3, 0, ['_',' ','-','.'])
    create_combobox(frame, "Info Delim", 2, 1, tab_name, "info_delim", 3, 1, ['-',' ','_','.'])
    create_combobox(frame, "Sub Delim", 2, 2, tab_name, "sub_delim", 3, 2, ['-',' ','_','.', '-_'])

    widgets[tab_name]["name_delim"].set('_')
    widgets[tab_name]["info_delim"].set('-')
    widgets[tab_name]["sub_delim"].set('-')

    widgets[tab_name]["lowercase"] = IntVar()
    lowercase_label = ctk.CTkLabel(frame, text="Case Sensitivity")
    lowercase_label.grid(row=4, column=0, columnspan=2)
    lowercase_check = ctk.CTkCheckBox(frame, variable=widgets[tab_name]["lowercase"], 
                                      onvalue=1, offvalue=0, 
                                      text="Lowercase Names", 
                                      command=lambda:update_example(widgets, example_text, get_selected_tab()))
    lowercase_check.grid(row=5, column=0, columnspan=2)

def build_series_tab(frame):
    format_options(frame, "series")

    widgets["series"]["episode"] = IntVar()
    episode_name_label = ctk.CTkLabel(frame, text="Episode Names")
    episode_name_label.grid(row=4, column=1, columnspan=2)
    episode_name_check = ctk.CTkCheckBox(frame, variable=widgets["series"]["episode"], 
                                         onvalue=1, offvalue=0, 
                                         text="Episode names in file name", 
                                         command=lambda:update_example(widgets, example_text, get_selected_tab()))
    episode_name_check.grid(row=5, column=1, columnspan=2)

def build_movie_tab(frame):
    format_options(frame, "movies")

def get_selected_tab():
    return type_tab.get().lower()

def get_media_type():
    selected_tab = get_selected_tab()
    return 1 if selected_tab == "series" else 0

build_movie_tab(movie_tab)
build_series_tab(series_tab)

for widget in series_tab.winfo_children():
    widget.grid_configure(padx=15, pady=5)

for widget in movie_tab.winfo_children():
    widget.grid_configure(padx=15, pady=5)

# Folder Selection
folder_frame = ctk.CTkFrame(frame)
folder_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

folder_label = ctk.CTkLabel(folder_frame, text="Enter or select directory")
folder_label.grid(row=0, column=0)

folder_entry = ctk.CTkEntry(folder_frame, width=300)
folder_entry.grid(row=1, column=0, columnspan=2)

browse_button = ctk.CTkButton(folder_frame,
                              text="Browse...",
                              command=lambda: folder_entry.insert(0, filedialog.askdirectory())
                              )
browse_button.grid(row=1, column=2)

folder_button = ctk.CTkButton(folder_frame,
                              text="Check Folder",
                              command=lambda:parse_folder(folder_entry, folder_list, preview_button)
                              )
folder_button.grid(row=2, column=0)

preview_button = ctk.CTkButton(folder_frame,
                               text="Preview",
                               command=lambda:insert_preview(folder_entry, preview_list, widgets, get_selected_tab(), rename_button),
                               state=DISABLED
                               )
preview_button.grid(row=2, column=1)

rename_button = ctk.CTkButton(folder_frame,
                              text="Rename",
                              command=lambda:rename_file(folder_entry, widgets, get_selected_tab()),
                              state=DISABLED
                              )
rename_button.grid(row=2, column=2)

for widget in folder_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Preview Section
folder_label = ctk.CTkFrame(frame)
folder_label.grid(row=3, column=0, padx=20, pady=20)

preview_label = ctk.CTkFrame(frame)
preview_label.grid(row=3, column=1, padx=20, pady=20)

folder_list = ctk.CTkTextbox(folder_label, width=500, height=300, state=DISABLED)
preview_list = ctk.CTkTextbox(preview_label, width=500, height=300, state=DISABLED)

for widget in folder_label.winfo_children():
    widget.grid_configure(padx=10, pady=10)

for widget in preview_label.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Binding and Function Calls

update_example(widgets, example_text, get_selected_tab())
