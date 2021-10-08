#!/usr/bin/env python

from tkinter import Tk    
from tkinter.filedialog import askopenfilename, askdirectory
from os import makedirs, path as OSPath
from pathlib import Path as PathParser
from shutil import copyfile

# make dialogue box not pop up
Tk().withdraw()

# function that copys the file and handles any errors that happen
def copyFile(src, dist):
    try:
        print(fr"Copying {src} as {dist}")
        makedirs(OSPath.dirname(dist), exist_ok=True)
        copyfile(src, dist)
        print("Successful!")
    except OSError as err:
        print(f"Error copying {src} as {dist} on renderer {renderer}. Reason {err}")

# List of render pcs. Order matters here, please ensure that the first dict belongs to the PC that the first file is on
# two typs here, NORMAL is a simple copy file, while COPY will copy and also make another copy to other pc
render_pc_paths = [ 
    { "type": "NORMAL", "pc_name": "Ds-01" },
    { "type": "NORMAL", "pc_name": "Ds-02" },
    { "type": "NORMAL", "pc_name": "Ds-03" },
    { "type": "NORMAL", "pc_name": "Ds-04" },
    { "type": "NORMAL", "pc_name": "Ds-05" },
    { "type": "NORMAL", "pc_name": "Ds-sound", "num_map": "6", "ignore": "VIDEO" },
    { "type": "COPY", "pc_name": "Ds-fisheye", "other_pc_name": "Ds-master", "orig_pc_map": "7", "other_pc_map": "0" }
]

# Name of start PC where the first file is
start_pc_name = render_pc_paths[0]['pc_name']

# Extensions of files that'll be copied
extensions = ["dsi", "mpg"]

# Ask for the first file
path_to_show = askopenfilename(title="Select Source File")

# If a person hits cancel and doesn't select a file, don't let them go further
if(path_to_show == ""):
    print("MISSING SOURCE FILE.")
    raise SystemExit(1)

# Try to see if we can read the first file, just to make sure if this works then all the other ones will most likely work.
try:
    open(path_to_show, 'r')
except OSError:
    print("Sorry boss! That file either doesn't exist, or I just cannot open it. Troubleshooting steps: ensure the file actually exists and update the files permissions")

# Path to the directory that the first file is in. Will be .replace'd later on to correspond to each renderer
source_folder=OSPath.dirname(path_to_show)

# Path to the directory that the file needs to be copied to. Will be .replace'd later on to correspond to each renderer
destination_folder=askdirectory(title="Select a destination directory")

# If a person hits cancel and doesn't select a folder, don't let them go further
if(destination_folder == ""):
    print("MISSING DEST.")
    raise SystemExit(1)

# Use PathPaser().stem to chop off the extension, then chop off the _01 from the show path so we can add our own numbers for each renderer.
show_name=PathParser(path_to_show).stem[:-3]

# For every extension in the extensions array, meaning do this for both dsi and mpg files
for extension in extensions:
    # Go through the list of renderers
    for index, renderer in enumerate(render_pc_paths, start=1):
        # In the event you only need to transport sound, skip the rest of this code if the extension isn't mpg which is sound.
        if("ignore" in renderer and renderer["ignore"] == "VIDEO" and extension == "dsi"): continue
        if(renderer['type'] == "NORMAL"):
            source_path = fr"{source_folder}/{show_name}_0{index}.{extension}".replace(start_pc_name, renderer['pc_name'])
            destination_path = fr"{destination_folder}/{show_name}_0{index}.{extension}".replace(start_pc_name, renderer['pc_name'])
            copyFile(source_path, destination_path)
        if(renderer['type'] == "COPY"):
            source_path = fr"{source_folder}/{show_name}_0{index}.{extension}".replace(start_pc_name, renderer['pc_name'])
            destination_path_1 = fr"{destination_folder}/{show_name}_0{renderer['orig_pc_map']}.{extension}".replace(start_pc_name, renderer['pc_name'])
            destination_path_2 = fr"{destination_folder}/{show_name}_0{renderer['other_pc_map']}.{extension}".replace(start_pc_name, renderer['other_pc_name'])
            copyFile(source_path, destination_path_1)
            copyFile(source_path, destination_path_2)


print("Successfully copied file to all renderers")
