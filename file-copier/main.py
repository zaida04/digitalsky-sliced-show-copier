# How to run this file:
# 1. Hit the Windows button on the bottom left
# 2. Type in "Command Prompt"
# 3. In the opened window, type "cd Desktop" (if the path of this file has changed from being on the desktop, then just navigate to the appropriate folder)
# 4. Type "python clone_file.py" and hit Enter
# 5. Answer the following questions.
# 6. Profit

# import the function that allows us to copy files
from shutil import copyfile

# This is a list of all the network drives. Should we get another renderer or axe one, just add/remove it from this list. The naming should be consistent with the ones already in there.
render_pc_paths = ["Ds-01", "Ds-02", "Ds-03", "Ds-04", "Ds-05"]

# This prompts us for the path to our asset.
path_to_asset = input("Enter your asset path: ")
try:
    open(path_to_asset, 'r')
except OSError:
    print("Sorry boss! That file either doesn't exist, or I just cannot open it. Troubleshooting steps: ensure the file actually exists and update the files permissions")

# This prompts us for what dir in the asset folder on the RENDER PC to put the file. 
# This is because all assets will go under that same asset directory, so we might as well save ourselves some trouble and just give the path from the asset folder
asset_dir = input("What folder in the Assets folder would you like to put this asset under? Put \"none\" if you want it in the base Assets folder: ")
if asset_dir.lower() == "none":
    asset_dir = ""
else:
    asset_dir = f"{asset_dir}\\"
    
# Name of the asset INCLUDING extension.
asset_name = input("What would you like the name to be?: ")

# Copy the file in every render PC.
for path in render_pc_paths:
    # Example path generated: \\Ds-01\e\DigitalSkyDM\Assets\EarthScienceLabs\bigmoon.png
	copyfile(path_to_asset, fr"\\{path}\e\DigitalSkyDM\Assets\{asset_dir}\{asset_name}")
