
import os
import tkinter as tk  # Import tkinter and alias it as tk
from PIL import Image, ImageTk


import sys

def show_splash(root, image_name, size=(600, 200), win_size=(700, 150), duration = 3000):
    root.withdraw()

    #Process Image File path
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    parent_path = os.path.dirname(base_path)
    img_path = os.path.join(parent_path, 'Assets',image_name)
    
    #Open Image File
    orig_img = Image.open(img_path)
    res_img  = orig_img.resize(size,Image.LANCZOS)
    img = ImageTk.PhotoImage(res_img)

    
    splash = tk.Toplevel(root)
    splash.title('Loading...')
    splash.overrideredirect(True)
    
    
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w - win_size[0]) // 2
    y = (screen_h - win_size[1]) // 2
    splash.geometry(f"{win_size[0]}x{win_size[1]}+{x}+{y}")
    
    
    splash_logo = tk.Frame(splash, padx = 10, pady = 10)
    splash_logo.grid(row = 0, column = 0)

    splash_title = tk.Frame(splash, padx = 10, pady = 10)
    splash_title.grid(row = 1, column = 0,sticky = 'nw')

    splash.image = img
    tk.Label(splash_logo, image=splash.image).grid(row=0, column=0, sticky='w')
    tk.Label(splash_title, text="SUBMITTAL ASSISTANT", font=("Arial", 14)).grid(row=1, column=0, sticky='nw')
    tk.Label(splash_title, text="version 0.0012", font=("Arial", 12)).grid(row=0, column=1, sticky='nsew')
    tk.Label(splash_title, text="created by: Oscar Simon Velasco", font=("Arial", 10)).grid(row=1, column=1, sticky='nsew')
    

    splash.update_idletasks()

    def splash_kill():
        splash.destroy()
        root.deiconify()

    splash.after(duration, splash_kill) 
    return splash, img

