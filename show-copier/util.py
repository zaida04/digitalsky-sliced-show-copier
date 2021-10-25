from shutil import copy
from os import makedirs, path as OSPath
import colorama
DEBUG = False
colorama.init()
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET

def good(input: str):
    print(GREEN + input + RESET)
def meh(input: str):
    print(YELLOW + input + RESET)
def bad(input: str):
    print(RED + input + RESET)

# function that copys the file and handles any errors that happen
def copyFile(src: str, dist: str, renderer: str) -> None:
    try:
        meh(fr"Copying {src} as {dist}")
        makedirs(OSPath.dirname(dist), exist_ok=True)
        copy(src, dist)
        good("Successful!")
    except OSError as err:
        bad(f"Error copying {src} as {dist} on renderer {renderer}. Reason {err}")

def parseConfig(conf, pc_list) -> None:
    for line in conf:
        # If a line is ENABLE_DEBUG, enable verbose logging
        if(line == "ENABLE_DEBUG"): 
            DEBUG = True
            meh("DEBUG HAS BEEN ENABLED")

        # Split the line by every space in the line
        args = line.split()

        # If the first word in the line is NORMAL
        if(args[0] == "NORMAL"):
            # Base of NORMAL dict
            temp = { "type": "NORMAL", "pc_name": args[1] }
            try: 
                # If there is a 3rd word in the list, treat it as the ignore extension
                if(args[2]): temp["ignore"] = args[2]

                # If there is a 4th word in the list, treat it as the custom number to set the destination slice number to
                if(args[3]): temp["num_map"] = args[3]
            # If args[2] or args[3] doesn't exist, don't worry about it.
            except IndexError:
                pass
            pc_list.append(temp)

        elif(args[0] == "COPY"):
            pc_list.append({ 
                "type": "COPY", 
                "pc_name": args[1],
                "orig_pc_map": args[2], 
                "other_pc_name": args[3], 
                "other_pc_map": args[4]
            })

def overwrite_prompt_b(path: str):
    return RED + fr"This file already exists on the destination {path}. Do you wish to overwrite it? Y/N: " + RESET

# Only print if debug mode is enabled.
def debug(input: str):
    if(DEBUG): meh(input)
