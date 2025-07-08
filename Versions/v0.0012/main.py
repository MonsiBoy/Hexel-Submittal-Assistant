
from tkinterdnd2 import TkinterDnD
import sys, os
ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'UI'))
sys.path.append(ui_path)
from UI.splash_screen import show_splash
from UI.title_maker_tab import create_title_tab
from UI.bookmark_maker_tab import create_bookmark_tab
from UI.menu_bar import menu_bar
from tkinter import ttk 
import tkinter as tk
import threading
import numpy
import pypdf

root = TkinterDnD.Tk()
root.title("Submittal Helper")
root.geometry("1200x1000")

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", foreground="black", background="white")

selected_path = tk.StringVar(value="")
header = menu_bar(root, selected_path)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

create_title_tab(notebook, selected_path, b_color = "lightgrey", )
create_bookmark_tab(notebook, selected_path, b_color = "lightgrey")

show_splash(root, "hexel_works.png", size=(600, 200), win_size=(700, 300), duration = 3000)
root.mainloop()