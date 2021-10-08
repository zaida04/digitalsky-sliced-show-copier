# `digitalsky-util-scripts`  
Utilities for file, io, button creation, asset management, and more for [DigitalSky DarkMatter](https://skyskan.com/products/digital-planetarium-systems/).

## ⚡ Usage
```
https://github.com/zaida04/digitalsky-util-scripts.git
cd digitalsky-util-scripts
python <script-to-run-folder>/main.py
```

## 📝 About
This collection of utilities was created for a DigitalSky renderer PC setup. At its current state, DarkMatter is a buggy and sometimes lacking piece of software, which this utility aims to solve by providing missing functionality.

## 📜 Scripts
### [`sliced-show-copier`](https://github.com/zaida04/digitalsky-util-scripts/blob/main/show-copier)
**Location:** [`show-copier/`](https://github.com/zaida04/digitalsky-util-scripts/blob/main/show-copier/main.py)  
**Description:** Copy all the sliced files corresponding to a renderer from one dir on the renderer to another.  

The purpose for this tool is to help move show `.dsi` and `.mpg` files split into 7 parts from one folder on a renderer to another folder on that same renderer and to also copy it to the `DS-MASTER` computer. Made so that others can easily adapt it for their own setup by simply editing the `render_pc_paths` list.

### [`multi-network-drive-file-copier`](https://github.com/zaida04/digitalsky-util-scripts/blob/main/file-copier)    
**Location:** [`file-copier/`](https://github.com/zaida04/digitalsky-util-scripts/blob/main/file-copier/main.py)  
**Description:** Copy a specific asset or other media file to all renderers in your setup.    

The purpose for this tool is to help copy your video, audio, button assets, and other files to all of your renderer PCs in one simple go.

## ✋ Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
  
## ⚖️ LICENSE
Entire repo and all scripts/subscripts licensed under the [MIT License](https://github.com/zaida04/digitalsky-util-scripts/blob/main/LICENSE)
  
