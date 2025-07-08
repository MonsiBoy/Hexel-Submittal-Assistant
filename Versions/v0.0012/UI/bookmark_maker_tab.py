import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES
from data_handling.data_handler import file_rec, process_pdf


def create_bookmark_tab(notebook,selected_path, b_color = "lightgrey"):
    
    file_data = tk.StringVar(value="")

    #Create Tab
    bookmark_tab = tk.Frame(notebook, bg=b_color)
    notebook.add(bookmark_tab, text="Bookmark Maker")

    #Create Frame
    drag_sect = tk.Frame(bookmark_tab, bg = b_color, padx = 10, pady = 10)
    drag_sect.grid(row = 0 , column = 0)

    drop_zone = tk.Label(drag_sect, text = "Drag PDF file here", bg = 'white', relief = "groove", width = 40,  height = 10)
    drop_zone.grid(column = 0, row = 0, padx = 10, pady = 10)

    scan_mark = tk.Button(drag_sect, text = "Scan", command = lambda: process_pdf(file_data, drop_zone, up_prog, selected_path))
    scan_mark.grid(column = 0, row = 2, padx=10, pady=10)
    
    up_prog = ttk.Progressbar(drag_sect,  mode = "indeterminate")
    up_prog.grid(row = 1, column = 0, pady = 10)
    up_prog.grid_remove()
    
    drop_zone.drop_target_register(DND_FILES)
    drop_zone.dnd_bind('<<Drop>>', lambda event: file_rec(event, drop_zone, file_data))






