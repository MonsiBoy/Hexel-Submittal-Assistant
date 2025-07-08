import tkinter as tk
from tkinter import ttk, messagebox
from data_handling.data_handler import input_data, create_title

# Shared data containers
item_entries = []
register_entries = []
item_list = {}
register_list = {}
row_counter1 = [0]
row_counter2 = [0]

def create_title_tab(notebook, selected_path, b_color="lightgrey"):
    global row_counter1, row_counter2, item_entries, register_entries

    title_tab = tk.Frame(notebook, bg=b_color)
    notebook.add(title_tab, text="Title Maker")

    # Layout Sections
    heading = tk.Frame(title_tab, bg=b_color, padx=10, pady=10)
    heading.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    text_boxes = tk.Frame(title_tab, bg=b_color, padx=10, pady=10)
    text_boxes.grid(row=1, column=0, sticky="nsew")

    register_container = tk.Frame(text_boxes, bg=b_color)
    register_container.grid(row=5, column=1, sticky="nsew")

    items_box = tk.Frame(title_tab, bg=b_color, padx=10, pady=10)
    items_box.grid(row=2, column=0, sticky="nsew")

    remarks_box = tk.Frame(title_tab, bg=b_color, padx=10, pady=10)
    remarks_box.grid(row=3, column=0, sticky="w")

    add_info = tk.LabelFrame(title_tab, text="Additional Information", bg=b_color, padx=10, pady=10, bd=1, relief="solid")
    add_info.grid(row=1, column=1, sticky="nw")

    # Label-entry helper
    def label_entry(row, label, parent):
        tk.Label(parent, text=label, font=("Arial", 10, "bold"), bg=b_color).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(parent, width=50)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    # Add new item row
    def add_text_box_items(button, row, item):
        button.grid_forget()
        row_c = row[0]

        item_entry = tk.Entry(items_box, width=50)
        page_start = tk.Entry(items_box, width=5)
        page_end = tk.Entry(items_box, width=5)

        item_entry.grid(row=row_c, column=1, padx=(92, 10), pady=5, sticky="nsew")
        page_start.grid(row=row_c, column=2, padx=10, pady=5, sticky="nsew")
        page_end.grid(row=row_c, column=4, padx=10, pady=5, sticky="nsew")

        tk.Label(items_box, text="~", font=("Arial", 10, "bold"), borderwidth=0, highlightthickness=0).grid(row=row_c, column=3, padx=10, pady=5, sticky="w")

        row[0] += 1
        button.grid(row=row[0], column=1, padx=(92, 10))
        item.append((item_entry, page_start, page_end))

    # Add new register row
    def add_text_box_register(button, row, item):
        button.grid_forget()
        row_c = row[0]

        register_item = tk.Entry(register_container, width=44)
        register_no = tk.Entry(register_container, width=5)

        register_no.grid(row=row_c, column=0, padx=(11, 0), pady=5)
        register_item.grid(row=row_c, column=1, padx=(1, 0), pady=5)
        item.append((register_no, register_item))

        row[0] += 1
        button.grid(row=row[0], column=1, padx=(0, 35))

    # Main Entries
    title_entry = label_entry(0, "Project Title", text_boxes)
    section_entry = label_entry(1, "Specification Section", text_boxes)
    section_title_entry = label_entry(2, "Section Title", text_boxes)
    sd_type_entry = label_entry(3, "SD No.", text_boxes)
    paragraph_entry = label_entry(4, "Paragraph", text_boxes)

    # Register section header
    tk.Label(text_boxes, text="Register Item", font=("Arial", 10, "bold"), bg=b_color).grid(row=5, column=0, padx=10, pady=5, sticky="w")

    # Item section header
    tk.Label(items_box, text="Item List", font=("Arial", 10, "bold"), bg=b_color).grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Remarks
    tk.Label(remarks_box, text="Remarks", font=("Arial", 10, "bold"), bg=b_color).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    remarks_text = tk.Text(remarks_box, height=10, width=100)
    remarks_text.grid(row=1, column=0, padx=10, pady=5)

    # Additional Info
    tk.Label(add_info, text="No. of Pages", bg=b_color).grid(row=0, column=0, sticky="w", padx=5)
    pages = tk.Entry(add_info, width=10)
    pages.grid(row=0, column=1)

    tk.Label(add_info, text="Page list text color", bg=b_color).grid(row=0, column=2, sticky="w", padx=10)
    color_options = ["Red", "Blue", "Yellow"]
    selected_color = tk.StringVar(value="Blue")
    color_drop = ttk.Combobox(add_info, textvariable=selected_color, values=color_options, state="readonly", width=10)
    color_drop.grid(row=0, column=3, padx=5, pady=5)

    # Buttons
    tk.Button(
        title_tab,
        text="Input Data",
        command=lambda: input_data(
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
        )
    ).grid(row=4, column=0, sticky='w', pady=10)

    tk.Button(
        title_tab,
        text="Submit",
        command=lambda: create_title(selected_path)
    ).grid(row=4, column=0, sticky='e')

    # Add buttons
    add_box = tk.Button(items_box, text="+", command=lambda: add_text_box_items(add_box, row_counter1, item_entries))
    add_box.grid(row=row_counter1[0], column=1, padx=(233, 10), pady=5)

    add_box_register = tk.Button(register_container, text="+", command=lambda: add_text_box_register(add_box_register, row_counter2, register_entries))
    add_box_register.grid(row=0, column=1, padx=152)

    return title_tab
