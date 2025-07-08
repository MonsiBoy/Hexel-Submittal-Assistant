import os
from tkinter import messagebox
import tkinter as tk
from Functions.Bookmark_Maker import bookmark_gen
from Functions.Title_Maker import generate_pdf
import threading

data = None
def file_rec(event, drop_zone, file_data):
    try:
        dropped_files = event.data
        cleaned_path = dropped_files.strip('{}')

        if not cleaned_path.lower().endswith(".pdf"):
            messagebox.showwarning("Wrong File Type", "Please input a PDF file")
            return
        
        drop_zone.config(text=f"Received:\n{os.path.basename(cleaned_path)}")
        file_data.set(cleaned_path)

        return cleaned_path
    
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}") 
        return   
def process_pdf(file_path, drop_zone, up_prog, selected_path):
    def run_processing():
        try:
            file = file_path.get()
            bookmark_gen(file, selected_path)
            drop_zone.after(0, lambda: [
                up_prog.stop(),
                up_prog.grid_remove(),
                drop_zone.config(text="Processing Complete!")
            ])
        except Exception as e:
            drop_zone.after(0, lambda e=e: messagebox.showerror("Error", f"Processing error:\n{e}"))

    up_prog.grid()
    up_prog.start()
    drop_zone.config(text="Please wait file is being scaned")

    threading.Thread(target=run_processing, daemon=True).start()   
def input_data(
    title_entry,
    register_list,
    section_entry,
    section_title_entry,
    sd_type_entry,
    paragraph_entry,
    register_entries,
    item_entries,
    remarks_text,
    pages,
    color_drop,
    item_list
):
    try:
        global data
        register_list.clear()
        item_list.clear()

        # Populate register entries
        for register_no, register_item in register_entries:
            key = register_no.get().strip()
            val = register_item.get().strip()
            if key:
                register_list[key] = val

        # Populate item entries
        for item_entry, page_start, page_end in item_entries:
            key = item_entry.get().strip()
            val_start = page_start.get().strip()
            val_end = page_end.get().strip()
            if key:
                item_list[key] = {"page_start": val_start, "page_end": val_end}

        # Build data dictionary
        data = {
            "title": title_entry.get().strip(),
            "section_number": section_entry.get().strip(),
            "section_title": section_title_entry.get().strip(),
            "sd_type": sd_type_entry.get().strip(),
            "paragraph": paragraph_entry.get().strip(),
            "register item": register_list,
            "item": item_list,
            "remarks": remarks_text.get("1.0", tk.END).strip(),
            "total pages": pages.get().strip(),
            "color": color_drop.get().strip(),
        }

        # Check for any empty required fields
        for key, value in data.items():
            if not value:
                messagebox.showwarning("Missing Information", f"Please complete the '{key}' field.")
                return
        messagebox.showinfo("Data has been saved", "Don't forget to submit")

        return data

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
def create_title(folder_selected):
    try:
        global data
        folder = folder_selected.get()

        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a destination folder.")
            return

        if not data:
            messagebox.showerror("Input Data Missing", f"Don't forget to press INPUT")    
        
        generate_pdf(data, folder)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")  