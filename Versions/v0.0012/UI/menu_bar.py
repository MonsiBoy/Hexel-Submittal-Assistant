import os
from tkinter import messagebox, filedialog
import tkinter as tk

def menu_bar(root, selected_path_var):
    bar = tk.Menu(root)
    file_menu = tk.Menu(bar, tearoff=0)

    def save_dest():
        path = filedialog.asksaveasfilename(
        title="Save File As...",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile="Output.pdf"  # optional default filename
    )   
        if path:
            selected_path_var.set(path)

    #file_menu.add_command(label="New")
    #file_menu.add_command(label="Open")
    #file_menu.add_command(label="Save")
    file_menu.add_command(label="Save Destination", command = save_dest)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command = root.quit)
    bar.add_cascade(label="File", menu=file_menu)
    root.config(menu=bar)

    #tk.Label(header, text="Save To:", bg="lightblue").pack(side="left", padx=10)
    #tk.Entry(header, textvariable=selected_path_var, width=50).pack(side="left", padx=5)
    #tk.Button(header, text="Browse", command=browse_folder).pack(side="left", padx=5)

    return bar