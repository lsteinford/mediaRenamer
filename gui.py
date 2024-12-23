#!/usr/bin/env python3
from tkinter import *
from tkinter import filedialog
import customtkinter as ctk
from tktooltip import ToolTip
from functions import update_example, parse_folder, insert_preview, rename_file

# Set theme and color options
ctk.set_appearance_mode("system") # Modes: system (default), light, dark
ctk.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

root = ctk.CTk()

global_font = ctk.CTkFont(family="Arial", size=16)
tab_font = ctk.CTkFont(family="Arial", size = 22)

root.title("Media Renamer")

frame = ctk.CTkFrame(root)
frame.pack()

# Example Text Section
example_frame = ctk.CTkFrame(frame)
example_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

example_label = ctk.CTkLabel(example_frame, text="Naming Convention Example", font=global_font)
example_label.grid(row=0, column=0)

example_text = ctk.CTkTextbox(example_frame, height=1, width=500, state=DISABLED, font=global_font)
example_text.grid(row=1, column=0, columnspan=2)

for widget in example_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Create tabs
type_tab = ctk.CTkTabview(frame, command=lambda:update_example(widgets, example_text, get_selected_tab(), rename_button), height=100)
type_tab.grid(row=0, column=0, columnspan=2)

series_tab = type_tab.add("Series")
movie_tab = type_tab.add("Movies")

type_tab._segmented_button.configure(font=tab_font)

widgets = {
    "series": {},
    "movies": {}
}

delim_options = ['_',' ','-','.']

# Create tab screens
def create_combobox(frame, label_text, label_row, label_col, tab_name, widget_name, widget_row, widget_col, values):
    # Label for combobox
    label = ctk.CTkLabel(frame, text=label_text, font=global_font)
    label.grid(row=label_row, column=label_col)
    # Create a combobox
    combobox = ctk.CTkComboBox(frame, values=values, font=global_font, command=lambda _:update_example(widgets, example_text, get_selected_tab(), rename_button))
    combobox.set("")
    combobox.grid(row=widget_row, column=widget_col)
    def custom_input(event=None):
        custom_value = combobox.get()
        if custom_value and custom_value not in values:
            values.append(custom_value)
            combobox.configure(values=values)
        update_example(widgets, example_text, get_selected_tab(), rename_button)
    combobox.bind("<Return>", custom_input)

    widgets[tab_name][widget_name] = combobox

def create_checkbox(frame, label_text, tab_name, widget_name, widget_row, widget_col):
    widgets[tab_name][widget_name] = IntVar()
    # Checkbox
    checkbox = ctk.CTkCheckBox(frame, variable=widgets[tab_name][widget_name], 
                                         onvalue=1, offvalue=0, 
                                         font=global_font, 
                                         text=label_text, 
                                         command=lambda:update_example(widgets, example_text, get_selected_tab(), rename_button))
    checkbox.grid(row=widget_row, column=widget_col)


def format_options(frame, tab_name):
    create_combobox(frame, "Name Delimiter", 2, 0, tab_name, "name_delim", 3, 0, delim_options)
    create_combobox(frame, "Info Delimiter", 2, 1, tab_name, "info_delim", 3, 1, delim_options)
    create_combobox(frame, "Sub Delimiter", 2, 2, tab_name, "sub_delim", 3, 2, delim_options)

    widgets[tab_name]["name_delim"].set("")
    widgets[tab_name]["info_delim"].set("")
    widgets[tab_name]["sub_delim"].set("")

    create_checkbox(frame, "Skip API", tab_name, "skipApi", 4, 0)
    create_checkbox(frame, "Lowercase Names", tab_name, "lowercase", 4, 1)

    custom_label = ctk.CTkLabel(frame, text="Custom Info Extension", font=global_font)
    custom_label.grid(row=5, column=1)
    custom_ext_entry = ctk.CTkEntry(frame, width=200)
    custom_ext_entry.grid(row=6, column=1)
    def custom_ext(event:None):
        update_example(widgets, example_text, get_selected_tab(), rename_button)
    custom_ext_entry.bind("<Return>", custom_ext)
    widgets[tab_name]["custom_ext"] = custom_ext_entry


def build_series_tab(frame):
    format_options(frame, "series")
    create_checkbox(frame, "Episode Names", "series", "episode", 4, 2)

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
    widget.grid_configure(padx=45, pady=7)

for widget in movie_tab.winfo_children():
    widget.grid_configure(padx=45, pady=7)

# Folder Selection
folder_frame = ctk.CTkFrame(frame)
folder_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

folder_label = ctk.CTkLabel(folder_frame, text="Enter or select directory", font=global_font)
folder_label.grid(row=0, column=0)

folder_entry = ctk.CTkEntry(folder_frame, width=300, font=global_font)
folder_entry.grid(row=1, column=0, columnspan=2)

def browse_folders():
    folder_entry.delete(0, ctk.END)
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_entry.insert(0, selected_folder)

browse_button = ctk.CTkButton(folder_frame, 
                              font=global_font,
                              text="Browse...",
                              command= browse_folders)
browse_button.grid(row=1, column=2)

folder_button = ctk.CTkButton(folder_frame, 
                              font=global_font,
                              text="Check Folder",
                              command=lambda:parse_folder(folder_entry, folder_list, preview_button)
                              )
folder_button.grid(row=2, column=0)

preview_button = ctk.CTkButton(folder_frame, 
                               font=global_font,
                               text="Preview",
                               command=lambda:insert_preview(folder_entry, preview_list, rename_button),
                               state=DISABLED
                               )
preview_button.grid(row=2, column=1)
ToolTip(preview_button, msg="Check the media tab before clicking preview", follow=True)

rename_button = ctk.CTkButton(folder_frame, 
                              font=global_font,
                              text="Rename",
                              command=lambda:rename_file(folder_entry),
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

folder_list = ctk.CTkTextbox(folder_label, width=500, height=300, state=DISABLED, font=global_font)
preview_list = ctk.CTkTextbox(preview_label, width=500, height=300, state=DISABLED, font=global_font)

for widget in folder_label.winfo_children():
    widget.grid_configure(padx=10, pady=10)

for widget in preview_label.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Binding and Function Calls

update_example(widgets, example_text, get_selected_tab(), rename_button)
