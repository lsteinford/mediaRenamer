#!/usr/bin/env python3
import os
import requests
import json
import re
from gui import *
from dotenv import load_dotenv 

load_dotenv()
apiKey = os.getenv("API_KEY")

def update_example(widget, example_text, selected_tab):
    
    name_delim = widget[selected_tab]["name_delim"].get()
    info_delim = widget[selected_tab]["info_delim"].get()
    sub_delim = widget[selected_tab]["sub_delim"].get()
    example_names = ["Movie","Name","Episode","Sub", "Series"]

    if widget[selected_tab]["lowercase"].get() == 1:
        example_names = [name.lower() for name in example_names]
            
    media_type = 1 if selected_tab == "series" else 0

    if media_type == 0:
        example = f"{example_names[0]}{name_delim}{example_names[1]}{sub_delim}{example_names[3]}{name_delim}{example_names[1]}{info_delim}YEAR.ext"
    else:
        if widget[selected_tab]["episode"].get() is not None and widget[selected_tab]["episode"].get() == 1:
            example = f"{example_names[4]}{name_delim}{example_names[1]}{sub_delim}{example_names[3]}{name_delim}{example_names[1]}{info_delim}S00E00{info_delim}{example_names[2]}{name_delim}{example_names[1]}.ext"
        else:
            example = f"{example_names[4]}{name_delim}{example_names[1]}{sub_delim}{example_names[3]}{name_delim}{example_names[1]}{info_delim}S00E00.ext"
    example_text.configure(state=NORMAL)
    example_text.delete("1.0", ctk.END) 
    example_text.insert(ctk.END, example)
    example_text.configure(state=DISABLED)

# Folder Functions

def parse_folder(folder_path, folder_list, preview_button):
    folder_list.configure(state=NORMAL)
    folder_list.delete("1.0", ctk.END)
    contents = os.listdir(folder_path.get())
    contents.sort()
    i = 1
    for item in contents:
        folder_list.insert(ctk.END, f"{item}\n")
    folder_list.configure(state=DISABLED)
    preview_button.configure(state=NORMAL)

def insert_preview(folder_path, preview_list, widget, selected_tab, rename_button):
    name_delim = widget[selected_tab]["name_delim"].get()
    info_delim = widget[selected_tab]["info_delim"].get()
    sub_delim = widget[selected_tab]["sub_delim"].get()
    lowercase = widget[selected_tab]["lowercase"].get()

    media_type = 1 if selected_tab == "series" else 0

    preview_list.configure(state=NORMAL)
    preview_list.delete("1.0", ctk.END)
    contents = os.listdir(folder_path.get())
    contents.sort()
    for item in contents:
        if media_type == 0:
            file_name = name_movie(item, name_delim, info_delim, sub_delim, lowercase)
        else:
            episode = widget[selected_tab]["episode"].get()
            file_name = name_series(item, name_delim, info_delim, sub_delim, episode, lowercase)
        preview_list.insert(ctk.END, f"{file_name}\n")
    rename_button.configure(state=NORMAL)

def rename_file(folder_entry, widget, selected_tab):
    name_delim = widget[selected_tab]["name_delim"].get()
    info_delim = widget[selected_tab]["info_delim"].get()
    sub_delim = widget[selected_tab]["sub_delim"].get()
    lowercase = widget[selected_tab]["lowercase"].get()
    media_type = 1 if selected_tab == "series" else 0

    folder_path = folder_entry.get()
    contents = os.listdir(folder_path)
    contents.sort()
    for item in contents:
        if media_type == 0:
            file_name = name_movie(item, name_delim, info_delim, sub_delim, lowercase)
        else:
            episode = widget[selected_tab]["episode"].get()
            file_name = name_series(item, name_delim, info_delim, sub_delim, episode, lowercase)
        old_name = f"{folder_path}/{item}"
        new_name = f"{folder_path}/{file_name}"
        os.rename(old_name, new_name)

# Movie Functions

# To do: else should search imdb for the year of the movie and pull it if needed
#        however, this will likely never be an issue since most files usually come
#        with the year in the file name
def extract_year(file_name):
    pattern = r"(\d{4})"
    match = re.search(pattern, file_name, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        print(f"Error extracting year from {file_name}")
        return None

def name_movie(file_name, name_delim, info_delim, sub_delim, lowercase):
    show_name = detect_name(file_name, name_delim, sub_delim)
    year = extract_year(file_name)
    file_ext = get_file_extension(file_name)
    file_name = f"{show_name}{info_delim}{year}{file_ext}"
    if lowercase == 1:
        return file_name.lower()
    else:
        return file_name

# Series Functions

def extract_season(file_name):
    pattern = r"(s\d{2}e\d{2})"
    match = re.search(pattern, file_name, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        print(f"Error extracting season from {file_name}. Did you forget to switch tabs?")
        return None

def search_episode_name(show_name, file_name):
    show_name = show_name.replace(" ","+")
    s00e00 = extract_season(file_name)
    season_number = s00e00[1:3]
    episode_number = s00e00[4:6]
    url=f"http://www.omdbapi.com/?apikey={apiKey}&t={show_name}&season={season_number}&episode={episode_number}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.text
    data = json.loads(data)
    episode_name = data['Title']
    return episode_name

def name_series(file_name, name_delim, info_delim, sub_delim, episode, lowercase):
    
    show_name = detect_name(file_name, name_delim, sub_delim).replace(".", name_delim).rstrip(name_delim)
    season = extract_season(file_name)
    file_ext = get_file_extension(file_name)
    if episode is not None and episode == 1:
        episode_name = search_episode_name(show_name, file_name).replace(" ", name_delim)
        file_name = f"{show_name.replace(".", name_delim).rstrip(name_delim)}{info_delim}{season}{info_delim}{episode_name}{file_ext}"
    else:
        file_name = f"{show_name.replace(".", name_delim).rstrip(name_delim)}{info_delim}{season}{file_ext}"
    if lowercase == 1:
        return file_name.lower()
    else:
        return file_name

def get_file_extension(file_name):
    _, extension = os.path.splitext(file_name)
    return extension

def detect_name(file_name, name_delim, sub_title_delim):
    
    pattern = r"(s\d{2}e\d{2})|(\d{4})"
    delim_pattern = r"[._ -]"
    sub_title_pattern = rf":{name_delim}?"

    match = re.search(pattern, file_name, re.IGNORECASE)

    if match:
        end_index = match.start()
        media_name = file_name[:end_index].strip(".,-_() !")
    else:
        media_name = file_name

    media_name = re.sub(pattern, "+", media_name)
    url=f"http://www.omdbapi.com/?apikey={apiKey}&t={media_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Use the title from OMDB if found
        if 'Title' in data:
            media_name = data['Title'].strip("?!")
    except (requests.RequestException, KeyError, json.JSONDecodeError):
        # Log or print an error for debugging if desired
        print("OMDB API call failed. Using file name instead.")
        media_name = file_name[:end_index].strip(".,-_() !")

    media_name = re.sub(delim_pattern, name_delim, media_name)
    media_name = re.sub(sub_title_pattern, sub_title_delim, media_name)

    print(media_name)

    return media_name      

def main():
    root.mainloop()

if __name__ == "__main__":
    main()