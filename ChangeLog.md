# v0.001
-


## v0.0012
- Added bookmark making funcionality
- removed non-functioning buttons in the file bar
- Default window size adjusted to fit all widgets

# v0.002 (MAJOR UPDATE)
The entire program has been ported over to the PySide6 library due to the growing limitations of the aging Tkinter. With this shift, the UI should feel much cleaner and more modern—overall, less clunky and more intuitive to use.

That being said, the Title Maker functionality has been temporarily removed in this version. I wasn’t satisfied with how it was implemented before and believe it deserves a better approach. I’ll be reworking it from the ground up. In the meantime, here are the current features in this version:
### Bookmark tab
- A much more flexible and intuitive hierarchical tree structure has been added—think something similar to PDF XChange’s “Bookmark Tree.” Nested bookmark management should now be a lot easier and less painful.

- You can now switch between different modes depending on your needs. Best of all, existing bookmarks can be read and modified—finally.

### New Tool Tab
This is a new area filled with small tools that may (or may not 😅) help speed up your workflow. I plan to add more over time as I stumble across repetitive and tedious tasks. If you have ideas or requests, please reach out! For now, it includes:
  #### **QR Scanner** 
  A simple but surprisingly hard-to-find tool—a desktop QR scanner. I was shocked by the lack of decent options out there, so here it is. Basic but incredibly useful.  
  #### **Text Scanner**, 
  Ever had a PDF where you just where you can’t for the love of god select the text no matter what you do? Same here. This tool captures text directly from your screen using OCR.       Currently, it uses EasyOCR, which works well enough for most cases. However, I’m working on adding PaddleOCR for more accurate scanning (especially for tables). Downside? Most of its documentation is in Chinese, so it’s a bit of a learning curve—but stay tuned!
 #### **Auto Directory Tree builder**, 
Need to generate a project folder tree quickly? This tool lets you do just that. I’ve included two ready-to-use templates. If you use a different format, let me know and I’ll bake your custom template into the next release. You can also optionally include a few industry-standard references. It’s not a full library (yet), but I’ll keep expanding it as I go. (Please note: these files are for personal reference only—take any precautions you need.) Currently the available references are:
- IEEE
  - C57 12 00
    - 2015
    - 2021
  - C57 12 28
    - 2023
  - C57 12 29
    - 2023
  - C57 12 30
    - 2020
- ANSI
  - C12.1
    - 2008
  - C12.10
    - 2011

The program is still very much a work in progress, built entirely during my free time. So I really appreciate your patience. If you have any feedback or features you’d like to see, don’t hesitate to reach out. I’ll also be posting a development roadmap sometime next month so you can see what’s in the pipeline!

## v0.0021
Released: 2025/07/28  
Update Notes:
### Feature updates
- Multithreading is now enabled in the Bookmarking Tab. PDF scanning should now be 10x faster.
- Text Scanning now supports multiple languages.
  - English
  - Japanese
  - Chinese (Simplified)
  - Chinese (Traditional)
  - German
  - Russian
  - Arabic
  - Korean
  - English & Japanese
### Bug Fixes
- In "scan and read" mode, a bug that causes the progress bar to misreport the progress has now been fixed. "Scanning" and "Reading" should now individually contribute 50% of the progress.
- A bug that prevents users from placing an item at the topmost level of the heirarchy has now been fixed.
### QoL Updates
- Some features now have feedback dialog boxes.
- A confirmation box will now prompt the user if the save destination of a bookmarked PDF is not changed from the previous run.
### Standard Library Additions
- IEEE
  - IEEE 386
    - 2006
    - 2016
