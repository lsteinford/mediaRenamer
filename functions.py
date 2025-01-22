#!/usr/bin/env python3
#This is a test pull
import os
import requests
import json
import re
from gui import *
from dotenv import load_dotenv 

load_dotenv()
apiKey = os.getenv("API_KEY")

name_delim = None
info_delim = None
sub_delim = None
episode = None
lowercase = None
skip_api = None
custom_ext = None
media_type = None

extensions = (".mkv", ".mp4", ".avi", ".wmv", ".mov", ".m4v")

def update_example(widget, example_text, selected_tab, rename_button):
    global name_delim, info_delim, sub_delim, episode, lowercase, skip_api, media_type, custom_ext
    name_delim = widget[selected_tab]["name_delim"].get()
    info_delim = widget[selected_tab]["info_delim"].get()
    sub_delim = widget[selected_tab]["sub_delim"].get()
    skip_api = widget[selected_tab]["skipApi"].get()
    lowercase = widget[selected_tab]["lowercase"].get()
    custom_ext = widget[selected_tab]["custom_ext"].get()

    example_names = ["Movie","Name","Episode","Sub", "Series"]

    if lowercase == 1:
        example_names = [name.lower() for name in example_names]
            
    media_type = 1 if selected_tab == "series" else 0

    base_ext = f"{info_delim}{custom_ext}.ext" if custom_ext else ".ext"

    base_movie = f"{example_names[0]}{name_delim}{example_names[1]}{sub_delim}{example_names[3]}{name_delim}{example_names[1]}{info_delim}YEAR"

    base_series = f"{example_names[4]}{name_delim}{example_names[1]}{sub_delim}{example_names[3]}{name_delim}{example_names[1]}{info_delim}S00E00"

    if media_type == 0:
        example = f"{base_movie}{base_ext}"
    else:
        episode = widget[selected_tab]["episode"].get()
        if episode is not None and episode == 1 and skip_api == 0:
            example = f"{base_series}{info_delim}{example_names[2]}{name_delim}{example_names[1]}{base_ext}"
        else:
            example = f"{base_series}{base_ext}"
    
    example_text.configure(state=NORMAL)
    example_text.delete("1.0", ctk.END) 
    example_text.insert(ctk.END, example)
    example_text.configure(state=DISABLED)
    rename_button.configure(state=DISABLED)

# Folder Functions

def parse_folder(folder_path, folder_list, preview_button):
    folder_list.configure(state=NORMAL)
    folder_list.delete("1.0", ctk.END)
    for entry in os.scandir(folder_path.get()):
        if entry.is_file() and entry.name.endswith(extensions):
            folder_list.insert(ctk.END, f"{entry.name}\n")
    folder_list.configure(state=DISABLED)
    preview_button.configure(state=NORMAL)

def insert_preview(folder_path, preview_list, rename_button):
    preview_list.configure(state=NORMAL)
    preview_list.delete("1.0", ctk.END)
    for item in os.scandir(folder_path.get()):
        if item.is_file() and item.name.endswith(extensions):
            if media_type == 0:
                file_name = name_movie(item.name)
            else:
                file_name = name_series(item.name)
            preview_list.insert(ctk.END, f"{file_name}\n")
    rename_button.configure(state=NORMAL)

def rename_file(folder_path):

    for item in os.scandir(folder_path.get()):
        if item.is_file() and item.name.endswith(extensions):
            if media_type == 0:
                file_name = name_movie(item.name)
            else:
                file_name = name_series(item.name)
            old_name = f"{folder_path.get()}/{item.name}"
            new_name = f"{folder_path.get()}/{file_name}"
            os.rename(old_name, new_name)

def re_format(data_info):
    # Default delimiters if not set
    global name_delim, sub_delim
    if not name_delim:
        name_delim = "."  # Default value
    if not sub_delim:
        sub_delim = "-"  # Default value
    
    # Patterns
    delim_pattern = r"[.,_ -+:/]"
    symbol_pattern = r"[?'!]"
    sub_title_pattern = rf":\s?|{re.escape(name_delim)}{{2,}}|:{re.escape(name_delim)}|{re.escape(name_delim)}-{re.escape(name_delim)}"
    
    try:
        # Remove single quotes and other special characters
        data_info = re.sub(symbol_pattern, "", data_info)
        # Replace general delimiters
        data_info = re.sub(delim_pattern, name_delim, data_info)
        # Replace subtitle patterns
        data_info = re.sub(sub_title_pattern, sub_delim, data_info)
        # Replace ampersand
        data_info = re.sub(r"&", "and", data_info)
    except re.error as e:
        print(f"Regex error: {e}")
    
    return data_info
# Movie Functions

# To do: else should search imdb for the year of the movie and pull it if needed
#        however, this will likely never be an issue since most files usually come
#        with the year in the file name
def extract_year(file_name):
    pattern = r"(?<=\s|[-_.(])\d{4}(?=\s|[-_.)]|$)"
    matches = re.findall(pattern, file_name)
    if matches:
        return matches[-1]
    else:
        print(f"Error extracting year from {file_name}")
        return None

def name_movie(file_name):
    ext = f"{info_delim}{custom_ext}" if custom_ext else ""

    show_name = detect_name(file_name)
    year = extract_year(file_name)
    file_ext = get_file_extension(file_name)
    file_name = f"{show_name}{info_delim}{year}{ext}{file_ext}"
    if lowercase == 1:
        return file_name.lower()
    else:
        return file_name

def extract_name(file_name):
    if media_type == 1:
        season = extract_season(file_name)
        end_index = file_name.find(season)
    else:
        year = extract_year(file_name)
        end_index = file_name.find(year)
    
    return file_name[:end_index].strip(".,-_() !")

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
    delim_pattern = r"( - )|(- )|(-_)|[.,_ -]"
    s00e00 = extract_season(file_name)
    season_number = s00e00[1:3]
    episode_number = s00e00[4:6]
    show_name = re.sub(delim_pattern, "+", show_name)
    url=f"http://www.omdbapi.com/?apikey={apiKey}&t={show_name}&season={season_number}&episode={episode_number}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.text
    data = json.loads(data)
    episode_name = data['Title']
    episode_name = re_format(episode_name)
    return episode_name

def name_series(file_name):
    ext = f"{info_delim}{custom_ext}" if custom_ext else ""
    
    show_name = extract_name(file_name)
    season = extract_season(file_name)
    file_ext = get_file_extension(file_name)
    if episode is not None and episode == 1 and skip_api == 0:
        episode_name = search_episode_name(show_name, file_name)
        show_name = re_format(show_name)
        file_name = f"{show_name}{info_delim}{season}{info_delim}{episode_name}{ext}{file_ext}"
    else:
        file_name = f"{show_name}{info_delim}{season}{ext}{file_ext}"
    if lowercase == 1:
        return file_name.lower()
    else:
        return file_name

def get_file_extension(file_name):
    _, extension = os.path.splitext(file_name)
    return extension

def detect_name(file_name):
    delim_pattern = r"[.,_ -]|(- )|(-_)"
    media_name = extract_name(file_name)

    if skip_api == 1:
        media_name = re_format(media_name)
        return media_name
    
    media_name = re.sub(delim_pattern, "+", media_name)
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

    media_name = re_format(media_name)

    return media_name      

def main():
    root.mainloop()

if __name__ == "__main__":
    main()