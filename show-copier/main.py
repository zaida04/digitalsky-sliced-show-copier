#!/usr/bin/env python

from tkinter import Tk    
from tkinter.filedialog import askopenfilename, askdirectory
from pathlib import Path as PathParser
from os import path as OSPath
from typing import List
from util import copyFile, parseConfig, overwrite_prompt_b, debug, bad, good, meh
import colorama
colorama.init()

# make dialogue box not pop up
Tk().withdraw()

# List of render pcs. Order matters here, please ensure that the first dict belongs to the PC that the first file is on
# two typs here, NORMAL is a simple copy file, while COPY will copy and also make another copy to other pc
render_pc_paths = [ 
    # { "type": "NORMAL", "pc_name": "Ds-01" },
    # { "type": "NORMAL", "pc_name": "Ds-02" },
    # { "type": "NORMAL", "pc_name": "Ds-03" },
    # { "type": "NORMAL", "pc_name": "Ds-04" },
    # { "type": "NORMAL", "pc_name": "Ds-05" },
    # { "type": "NORMAL", "pc_name": "Ds-sound", "num_map": "6", "ignore": "VIDEO" },
    # { "type": "COPY", "pc_name": "Ds-fisheye", "other_pc_name": "Ds-master", "orig_pc_map": "7", "other_pc_map": "0" }
]

# Open up and read config file
try:
    config_file = open("config.txt", mode="r")
    good("Found config file, reading...")
except FileNotFoundError:
    bad("You are missing the config.txt file. It should be in the same folder as this script. Exiting...")
    raise SystemExit(1)

# Turn the config into the render_pc_paths array
try:
    parseConfig(config_file, render_pc_paths)
    good("Successfully loaded config file!")
except Exception as Err:
    bad(Err)
    bad("There was an error parsing the config. Please contact the developer with the above output. Exiting...")
    raise SystemExit(1)

# Name of start PC where the first file is
start_pc_name: str = render_pc_paths[0]['pc_name']

# Extensions of files that'll be copied
extensions: List[str] = ["dsi", "mpg"]

# Ask for the first file
path_to_show: str = askopenfilename(title="Select Source File")
debug(meh(fr"Path to show: {path_to_show}"))

# If a person hits cancel and doesn't select a file, don't let them go further
if(path_to_show == ""):
    bad("MISSING SOURCE FILE.")
    raise SystemExit(1)

# Try to see if we can read the first file, just to make sure if this works then all the other ones will most likely work.
try:
    open(path_to_show, mode='r')
except OSError:
    bad("Sorry boss! That file either doesn't exist, or I just cannot open it. Troubleshooting steps: ensure the file actually exists and update the files permissions")

# Path to the directory that the first file is in. Will be .replace'd later on to correspond to each renderer
source_folder: str = OSPath.dirname(path_to_show)

# Path to the directory that the file needs to be copied to. Will be .replace'd later on to correspond to each renderer
destination_folder: str = askdirectory(title="Select a destination directory")
debug(meh(fr"Destination directory: {destination_folder}"))

# If a person hits cancel and doesn't select a folder, don't let them go further
if(destination_folder == ""):
    bad("MISSING DEST.")
    raise SystemExit(1)

# Use PathPaser().stem to chop off the extension, then chop off the _01 from the show path so we can add our own numbers for each renderer.
show_name: str = PathParser(path_to_show).stem[:-3]

# For every extension in the extensions array, meaning do this for both dsi and mpg files
for extension in extensions:
    # Go through the list of renderers
    for index, renderer in enumerate(iterable=render_pc_paths, start=1):
        debug(meh(fr"Working on renderer: {renderer} with index {index} on file {extension}"))
        pc_name = renderer["pc_name"]
        
        # In the event you only need to transport sound, skip the rest of this code if the extension isn't mpg which is sound.
        if("ignore" in renderer and renderer["ignore"] == "VIDEO" and extension == "dsi"): continue

        # Construct the path to the source folder
        source_path = fr"{source_folder}/{show_name}_0{index}.{extension}".replace(start_pc_name, renderer['pc_name'])
        
        if(renderer['type'] == "NORMAL"):
            # Replace path with the destinaton PC and the destination path along with the slice number.
            destination_path = fr"{destination_folder}/{show_name}_0{index}.{extension}".replace(start_pc_name, renderer['pc_name'])

            # Check if the file exists.
            if(PathParser(destination_path).is_file()):
                # If it does, ask if we want to replace it.
                if(input(overwrite_prompt_b(destination_path)).lower() != "y"): continue
            copyFile(source_path, destination_path, pc_name)
        
        elif(renderer['type'] == "COPY"):
            # Destination 1
            destination_path_1 = fr"{destination_folder}/{show_name}_0{renderer['orig_pc_map']}.{extension}".replace(start_pc_name, renderer['pc_name'])
            # Destination 2 - same file as dest 1 but just different slice number
            destination_path_2 = fr"{destination_folder}/{show_name}_0{renderer['other_pc_map']}.{extension}".replace(start_pc_name, renderer['other_pc_name'])

            # If dest 1 exists, ask if we want to replace it
            if(PathParser(destination_path_1).is_file()):
                if(input(overwrite_prompt_b(destination_path_1)).lower().strip() != "y"): continue

            # If dest 2 exists, ask if we want to replace it
            if(PathParser(destination_path_2).is_file()):
                if(input(overwrite_prompt_b(destination_path_2)).lower().strip() != "y"): continue

            copyFile(source_path, destination_path_1, pc_name)
            copyFile(source_path, destination_path_2, pc_name)

print("File copying completed.")
