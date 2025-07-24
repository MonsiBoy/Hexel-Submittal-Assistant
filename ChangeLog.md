## v0.001
-


## v0.0012
- Added bookmark making funcionality
- removed non-functioning buttons in the file bar
- Default window size adjusted to fit all widgets

## v0.002 (MAJOR UPDATE)
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
Need to generate a project folder tree quickly? This tool lets you do just that. I’ve included two ready-to-use templates. If you use a different format, let me know and I’ll bake your custom template into the next release. You can also optionally include a few industry-standard references. It’s not a full library (yet), but I’ll keep expanding it as I go. (Please note: these files are for personal reference only—take any precautions you need.)

The program is still very much a work in progress, built entirely during my free time. So I really appreciate your patience. If you have any feedback or features you’d like to see, don’t hesitate to reach out. I’ll also be posting a development roadmap sometime next month so you can see what’s in the pipeline!
 
