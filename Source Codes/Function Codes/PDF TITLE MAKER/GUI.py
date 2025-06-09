from ast import For
from atexit import register
import os
import select
from sqlite3 import Row
import tkinter as tk  # Import tkinter and alias it as tk
from tkinter import ttk
from Submittal_Maker import generate_pdf
from tkinter import Tk, filedialog, messagebox
from PIL import Image, ImageTk
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(base_path, "hexel_works.png")
orig_img = Image.open(img_path)

screen_width = 1000
screen_height = 1000
b_color = "lightgrey"
row_counter1 = 0
row_counter2 = 5
item_list ={}
item_entries = []
register_entries = []
register_list = {}
folder_selected = None
data            = None


res_img  = orig_img.resize((600,200),Image.LANCZOS)

root = tk.Tk()
root.configure(bg = b_color)
root.title("Submittal Helper")
root.geometry(f"{screen_width}x{screen_height}")
root.withdraw()

splash = tk.Toplevel()
splash.title('Loading...')
splash.geometry('700x150')
splash.overrideredirect(True)
img = ImageTk.PhotoImage(res_img)
splash_logo = tk.Frame(splash, padx = 10, pady = 10)
splash_logo.grid(row = 0, column = 0)

splash_title = tk.Frame(splash, padx = 10, pady = 10)
splash_title.grid(row = 1, column = 0,sticky = 'nw')

#splash_author = tk.Frame(splash, padx = 10, pady = 10)
#splash_author.grid(row = 1, column = 1)

tk.Label(splash_logo, image = img).grid(row = 0, column = 0, sticky = 'w')
tk.Label(splash_title, text="SUBMITTAL ASSISTANT", font=("Arial", 14)).grid(row = 1, column = 0, sticky = 'nw')
tk.Label(splash_title, text="version 0.001", font=("Arial", 12)).grid(row = 0, column = 1, sticky = 'nsew')
tk.Label(splash_title, text="created by: Oscar Simon Velasco", font=("Arial", 10)).grid(row = 1, column = 1, sticky = 'nsew')

splash.update_idletasks()
width = 1000
height = 300
x = (splash.winfo_screenwidth() // 2) - (width // 2)
y = (splash.winfo_screenheight() // 2) - (height // 2)
splash.geometry(f"{width}x{height}+{x}+{y}")

heading = tk.Frame(root, bg = b_color, padx=10, pady=10)
heading.grid(row = 0, column = 0, padx=20, pady=20, sticky="w")

text_boxes = tk.Frame(root, bg = b_color, padx=10, pady=10)
text_boxes.grid(row = 1, column = 0, sticky="nsew")
register_container = tk.Frame(text_boxes, bg = b_color)

items_box = tk.Frame(root, bg = b_color, padx=10, pady=10)
items_box.grid(row = 2, column = 0, sticky="nsew")

remarks_box = tk.Frame(root, bg = b_color, padx=10, pady=10)
remarks_box.grid(row = 3, column = 0, sticky="w")

add_info = tk.LabelFrame(root, text="Additional Information", bg = b_color, padx=10, pady=10, bd=1, relief="solid")
add_info.grid(row = 1, column = 1, sticky="nw")

folder_path = tk.StringVar()
folder_path.set("No folder selected")

def splash_byebye():
    splash.destroy()
    root.deiconify() 
def add_text_box_items(event = None):
    global row_counter1, item_entries

    add_box.grid_forget()

    item_entry = tk.Entry(items_box, width = 50)
    page_start = tk.Entry(items_box, width = 5)
    page_end = tk.Entry(items_box, width = 5)

    item_entry.grid(row = row_counter1, column = 1,padx=(92,10), pady=5, sticky="nsew")
    page_start.grid(row = row_counter1, column = 2,padx=10, pady=5, sticky="nsew")
    page_end.grid(row = row_counter1, column = 4,padx=10, pady=5, sticky="nsew")

    tk.Label(items_box, text="~", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=row_counter1, column=3, padx=10, pady=5, sticky="w")
    row_counter1 += 1
    
    add_box.grid(row = row_counter1, column = 1, padx=(92,10))
    item_entries.append((item_entry, page_start, page_end))
def add_text_box_register(event = None):
    global row_counter2, register_entries
    register_container = tk.Frame(text_boxes, bg = "b_color")
    
    add_box_register.grid_forget()
    register_container.grid(row = row_counter2, column = 1, sticky="w")
    register_item = tk.Entry(register_container, width = 44)
    register_no = tk.Entry(register_container, width = 5)


    
    register_no.grid(row = 0, column = 0,padx=(11,0), pady=5)
    register_item.grid(row = 0, column = 1, padx=(1,0), pady=5)
    register_entries.append((register_no,register_item))

    row_counter2 +=1

    add_box_register.grid(row = row_counter2, column = 1)
def new_file():
    print("New File created")
def open_file():
    print("File opened")
def save_file():
    print("File saved")
def choose_dest():
    global folder_selected

    folder_selected = filedialog.asksaveasfilename(
        title="Save PDF As...",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile="output.pdf"  # optional default filename
    )
    if folder_selected:
        
        folder_path.set(f"Folder selected: {folder_selected}")
        print(folder_path.get())
    else: 
        folder_path.set("No folder selected")       
def input_data(event = None):
    try:
        global item_list, item_entries, register_entries, register_list, data,folder_selected

        if not folder_selected:
            messagebox.showwarning("No Folder Selected", "Please select a destination folder.")
            return

        if register_list:
            register_list.clear()

        if item_list:
            item_list.clear()

        for register_no, register_item in register_entries:
            key  = register_no.get()
            val1 = register_item.get()
        
            if key:
                register_list[key] = val1

        for item_entry, page_start, page_end in item_entries:
            key = item_entry.get()
            val1 = page_start.get()
            val2 = page_end.get()
        
            if key:
                item_list[key] = {"page_start": val1, "page_end": val2}
        if data:
            data.clear()
        data = {
            "title": title_entry.get(),
            "section_number": section_entry.get(),
            "section_title": section_title_entry.get(),
            "sd_type": sd_type_entry.get(),
            "paragraph": paragraph_entry.get(),
            "register item": register_list,
            "item": item_list,
            "remarks": remarks_text.get("1.0", tk.END),  # from Text widget
            "total pages": pages.get(),
            "color": color_drop.get(),
        }
        for key, value in data.items(): 
            if not value:
               messagebox.showwarning("Missing Information", "Please complete all fields")
               return

        print(f'Data Saved: {data}')
        messagebox.showinfo("Data has been saved","Dont't forget to submit")
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")   
def create(event = None):
    global data, folder_selected
    print(f'data{data}')
    print(f'folder {folder_selected}')
    generate_pdf(data, folder_selected)

splash.after(3000, splash_byebye) 


file_bar = tk.Menu(heading)
file_menu = tk.Menu(file_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save Destination", command=choose_dest)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
file_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=file_bar)



status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
status_frame.grid(row = 99, column = 0, columnspan=999, sticky = 'we')

status = tk.Label(status_frame, textvariable=folder_path, anchor="w")
status.grid(row = 0, column = 0, sticky = 'we')

tk.Label(text_boxes, text="Project Title", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=0, column=0, padx=10, pady=5, sticky="w")
title_entry = tk.Entry(text_boxes, width = 50)
title_entry.grid(row = 0, column = 1, padx=10, pady=5)

tk.Label(text_boxes, text="Specification Section", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=1, column=0, padx=10, pady=5, sticky="w")
section_entry = tk.Entry(text_boxes, width = 50)
section_entry.grid(row = 1, column = 1,padx=10, pady=5)

tk.Label(text_boxes, text="Section Title", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=2, column=0, padx=10, pady=5, sticky="w")
section_title_entry = tk.Entry(text_boxes, width = 50)
section_title_entry.grid(row = 2, column = 1,padx=10, pady=5)

tk.Label(text_boxes, text="SD No.", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=3, column=0, padx=10, pady=5, sticky="w")
sd_type_entry = tk.Entry(text_boxes, width = 50)
sd_type_entry.grid(row = 3, column = 1,padx=10, pady=5)

tk.Label(text_boxes, text="Paragraph", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=4, column=0, padx=10, pady=5, sticky="w")
paragraph_entry = tk.Entry(text_boxes, width = 50)
paragraph_entry.grid(row = 4, column = 1,padx=10, pady=5)

tk.Label(text_boxes, text="Register Item ", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=5, column=0, padx=10, pady=5, sticky="w")
register_item = tk.Entry(register_container, width = 38)
register_no = tk.Entry(register_container, width = 10)

tk.Label(items_box, text="Item List", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=0, column=0, padx=10, pady=5, sticky="w")
item_entry = tk.Entry(items_box, width = 50)
page_start = tk.Entry(items_box, width = 10)
page_end = tk.Entry(items_box, width = 10)

tk.Label(remarks_box, text="Remarks", font=("Arial", 10, "bold"), bg = root["bg"], borderwidth=0, highlightthickness=0).grid(row=0, column=0, padx=10, pady=5, sticky="w")
remarks_text = tk.Text(remarks_box, height = 10, width = 100)
remarks_text.grid(row = 1, column = 0,padx=10, pady=5)

tk.Label(add_info, text="No. of Pages", bg = root["bg"]).grid(row=0, column=0, sticky="w",padx=(5,5))
pages = tk.Entry(add_info, width = 10)
pages.grid(row=0, column=1)

color_options = ['Red', 'Blue', 'Yellow']
selected_color = tk.StringVar()
tk.Label(add_info, text="Page list text color", bg = root["bg"] ).grid(row=0, column=2, sticky="w",padx=(10,5), pady=5)
color_drop = ttk.Combobox(add_info, textvariable=selected_color, values=color_options, state="readonly")
color_drop.grid(row = 0, column= 3, sticky='w',padx=5, pady=5)

add_box =tk.Button(items_box, text = "+", command = add_text_box_items)
add_box.grid(row = row_counter1, column = 1,padx=(233,10), pady=5)

add_box_register =tk.Button(text_boxes, text = "+", command = add_text_box_register)
add_box_register.grid(row = row_counter2, column = 1)

submit_button =tk.Button(root, text = "Submit", command = create)
submit_button.grid(row = 4, column = 0, sticky = 'e' )
submit_button =tk.Button(root, text = "Input Data", command = input_data)
submit_button.grid(row = 4, column = 0, sticky = 'w' )



root.mainloop()