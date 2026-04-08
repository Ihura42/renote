import customtkinter as ctk
from pathlib import Path
from tkcalendar import Calendar
from datetime import datetime
import os
import json

ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title('Renote')
root.geometry("1100x700")

root.bind("<Control-n>", lambda e: execute_command('New note'))
root.bind("<Control-s>", lambda e: execute_command('Save file'))

BG = "#1e1e1e"
SIDEBAR_BG = "#202020"
EXPLORER_BG = "#2a2a2a"
FILES_BG = "#303030"

SAVE_PATH = r"save"

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#main containers

sidebar = ctk.CTkFrame(root, width=60, fg_color=SIDEBAR_BG, corner_radius=0)
sidebar.pack(side='left', fill='y')

file_explorer = ctk.CTkFrame(root, width=200, fg_color=EXPLORER_BG, corner_radius=0)
file_explorer.pack(side='left', fill='y')

main = ctk.CTkFrame(root, fg_color=BG, corner_radius=0)
main.pack(side='right', fill='both', expand=True)

address_bar = ctk.CTkFrame(main, fg_color='#232323', height=40, corner_radius=0)
address_bar.pack(fill="x", side="top")

footer_bar = ctk.CTkFrame(main, fg_color='#232323', height=20, corner_radius=0)
footer_bar.pack(fill="x", side="bottom")

main_content = ctk.CTkFrame(main, fg_color=BG)
main_content.pack(fill="both", expand=True)

newfiles_amount = 1
current_file_path = None
current_text_area = None
current_title = None
current_page = 0

calendar_dates = {}


#showing main page content

def show_page(page_name):
    global current_page, current_text_area, current_title, current_file_path
    current_page = page_name

    for child in main_content.winfo_children():
        child.destroy()

    # reset current file references
    current_file_path = None
    current_text_area = None
    current_title = None

    if page_name == 'Home':
        title = ctk.CTkEntry(main_content, font=("Segoe UI", 28, "bold"), width=600, fg_color='transparent', border_width=0)
        title.insert("0", "Untitled")
        title.pack(pady=(50, 0), padx=(100, 0), anchor="w")

        text_area = ctk.CTkTextbox(main_content, font=("Segoe UI", 16))
        text_area.insert("0.0", "New text...")
        text_area.pack(fill='both', expand=True, padx=100, side='top')

        current_title = title
        current_text_area = text_area

    elif page_name == 'Notes':
        notes_title = ctk.CTkEntry(main_content, font=("Segoe UI", 28, "bold"), width=600, fg_color='transparent', border_width=0)
        notes_title.insert("0", "Notes")
        notes_title.pack(pady=(50, 0), padx=(100, 0), anchor="w")

        notes_list_frame = ctk.CTkFrame(main_content, fg_color='#2a2a2a', corner_radius = 8)
        notes_list_frame.pack(pady = 20, padx = 100, anchor = 'w', fill = 'x')

        note_files = [f for f in os.listdir(SAVE_PATH) if f.endswith(".md")]

        if not note_files:
            ctk.CTkLabel(notes_list_frame, text = 'no notes yet', font = ('Segoe UI', 14), text_color= "#666666").pack(pady = 20, padx = 20)
        else:
            for name in note_files:
                row = ctk.CTkFrame(notes_list_frame, fg_color="transparent")
                row.pack(fill = 'x', padx = 10, pady = 4)

                ctk.CTkButton(row, text= name.replace(".md", ""), anchor = 'w', fg_color=  'transparent', hover_color = '#333333', font = ("Segoe UI", 15), cursor = "hand2", command = lambda n = name: open_file(n)).pack(side = 'left', fill ='x', expand = True)
                ctk.CTkButton(row, text = 'x', width = 30, fg_color="#424242", hover_color="#353535", cursor = 'hand2', command = lambda n= name: [delete_file(n), show_page("Notes")]).pack(side = 'right')
    elif page_name == 'Calendar':
        calendar_title = ctk.CTkEntry(main_content, font=("Segoe UI", 28, "bold"), width=600, fg_color='transparent', border_width=0)
        calendar_title.insert("0", "Calendar")
        calendar_title.pack(pady=(50, 0), padx=(100, 0), anchor="w")

        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        calendar = Calendar(
            main_content,
            font=("Segoe UI", 16),
            selectmode='day',
            year=current_year,
            month=current_month,
            day=current_day,
            background="#2a2a2a",
            foreground="#ffffff"
        )
        calendar.pack(pady=30, anchor = 'w', padx = 100)

        calendar_entry = ctk.CTkEntry(
            main_content,
            font=("Segoe UI", 18),
            width=300,
            fg_color="#2a2a2a",
            border_width=1,
            border_color="#3a3a3a",
            placeholder_text="Write a note for this date..."
        )
        calendar_entry.pack(pady=5, anchor = 'w', padx = 135)
        def data_export():
            try:
                with open("data.json", mode='r', encoding='utf-8') as feedsjson:
                    feeds = json.load(feedsjson)
            except FileNotFoundError:
                feeds = []

            entry = {calendar.get_date():calendar_entry.get()}

            with open("data.json", 'w') as f:
                json.dump(entry, f, indent=4)

            feeds.append(entry)

            with open("data.json", mode='w', encoding='utf-8') as feedsjson:
                json.dump(feeds, feedsjson, indent=4)

            grad_date()
        

        date_label = ctk.CTkLabel(main_content, text="No date selected", font=("Segoe UI", 13), text_color="#aaaaaa")
        date_label.pack(pady=2,anchor = 'w', padx = 220)

        def grad_date():
            selected = calendar.get_date()

            if not os.path.exists("data.json"):
                date_label.configure(text=f"Selected day: {selected} — no notes yet")
                return

            with open('data.json', 'r') as file:
                data = json.load(file) 

            # search through each dict in the list for the selected date - claude
            note_text = next((item[selected] for item in data if selected in item), "")

            calendar_dates[selected] = note_text
            date_label.configure(
                text=f"Selected day: {selected}" + (f"  —  {note_text}" if note_text else "")
            )

        btn_frame = ctk.CTkFrame(main_content, fg_color= BG)
        btn_frame.pack(fill="x", pady=5)

        get_date_btn = ctk.CTkButton(
            btn_frame,
            text="Write note",
            command=data_export,
            width=150,
            fg_color="#333333",
            hover_color="#444444"
        )
        
        show_data_btn = ctk.CTkButton(
            btn_frame,
            text = 'Show note',
            command = grad_date,
            width = 150,
            fg_color = '#333333',
            hover_color = '#444444'
        )

        show_data_btn.pack(side="left", padx=95)

        get_date_btn.pack(side="left", padx=0)

    else:
        lbl = ctk.CTkLabel(main_content, text=page_name, font=("Segoe UI", 32))
        lbl.pack(expand=True)

def execute_command(command):
    global newfiles_amount
    if command == 'New note':
        new_name = f"newfile{newfiles_amount}.md"
        file_path = os.path.join(SAVE_PATH, new_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        refresh_files()
        open_file(new_name)
        newfiles_amount += 1

    if command == 'New todo list':
        create_todolist()

    if command == 'Delete file':
        if current_file_path:
            name = os.path.basename(current_file_path)
            delete_file(name)

    if command == 'Save file' and current_file_path:
        save_file(current_file_path, current_text_area, current_title)


# save file
def save_file(file_path, text_area, title):
    if not file_path:
        return

    # check widgets still exist
    try:
        current_filename = title.get().strip()
        current_content = text_area.get("1.0", 'end-1c')
    except Exception:
        return

    filename = os.path.basename(file_path).replace(".md", "")

    if current_filename != filename:
        new_path = os.path.join(SAVE_PATH, current_filename + ".md")
        os.rename(file_path, new_path)
        file_path = new_path
        print(f"Renamed to: {new_path}")

        # update the global link
        global current_file_path
        current_file_path = file_path
        refresh_files()

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(current_content)

    print(f"Auto-saved: {file_path}")

    # timer for autosave with file_path
    root.after(5000, save_file, file_path, text_area, title)


# opening file and showing in main

def open_file(name):
    global current_file_path, current_text_area, current_title
    for child in main_content.winfo_children():
        child.destroy()

    title = ctk.CTkEntry(main_content, font=("Segoe UI", 28, "bold"), width=600, fg_color='transparent', border_width=0)
    title.insert("0", name.replace(".md", ""))

    title.pack(pady=(50, 0), padx=(100, 0), anchor="w")

    file_path = os.path.join(SAVE_PATH, name)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    text_area = ctk.CTkTextbox(main_content, font=("Segoe UI", 16))
    text_area.insert("0.0", content)
    text_area.pack(fill='both', expand=True, padx=100, side='top')

    current_file_path = file_path
    current_text_area = text_area
    current_title = title

    root.after(5000, save_file, file_path, text_area, title)

# delete files

def delete_file(name):
    global current_file_path, current_text_area, current_title
    os.remove(SAVE_PATH + '/' + name)
    # clear editor if the deleted file was open
    if current_file_path and os.path.basename(current_file_path) == name:
        current_file_path = None
        current_text_area = None
        current_title = None
        for child in main_content.winfo_children():
            child.destroy()
    refresh_files()

def create_todolist():
    if current_text_area:
        current_text_area.insert("end", "- ☐ New Task\n")

        


# explorer container inside

explorer_header = ctk.CTkFrame(file_explorer, fg_color="transparent")
explorer_header.pack(fill="x", side="top", padx=5, pady=5)

explorer_file_list = ctk.CTkFrame(file_explorer, fg_color=FILES_BG)
explorer_file_list.pack(fill='both', expand=True)

#lists of buttons(icons)

buttons = [
    ("⌂", "Home"), ("📄", "Notes"), ("📅", "Calendar"),
]

explorer_icons = [("📄+", "New note"),
                  ("📁+", "New folder")]

address_bar_btns = [('X', 'Delete file'),
                    ('💾', "Save file"),
                    ("☑", 'New todo list')]



#importing files from folder

files = []
def refresh_files():
    files.clear()

    for filename in os.listdir(SAVE_PATH):
        if filename.endswith(".md"):
            files.append(filename)

    for child in explorer_file_list.winfo_children():
        child.destroy()

    for name in files:

        file_placer = ctk.CTkFrame(explorer_file_list, fg_color=FILES_BG)
        file_placer.pack(fill='y')
        file_line = ctk.CTkButton(file_placer, text=f"{ name }",
                                  anchor='w', hover_color="#333333",
                                  height=30,
                                  fg_color=FILES_BG,
                                  cursor='hand2',
                                  command=lambda n=name: open_file(n))
        file_line.pack(side='left', pady=5, padx=10)

        delete_button = ctk.CTkButton(file_placer, text="x",
                                      hover_color="#353535",
                                      fg_color='#424242',
                                      width=30,
                                      cursor='hand2',
                                      command=lambda n=name: delete_file(n))
        delete_button.pack(side='left', padx=(0, 20))
refresh_files()


#adding icons to sidebar

for icon, name in buttons:
    btn = ctk.CTkButton(
        sidebar,
        text=icon,
        width=40,
        height=40,
        fg_color="transparent",
        hover_color="#333333",
        font=("Segoe UI Symbol", 18),
        command=lambda n=name: show_page(n)
    )
    btn.pack(pady=5, padx=5)

#adding icons(buttons) to explorer

for icon, name in explorer_icons:
    small_btn = ctk.CTkButton(
        explorer_header,
        text=icon,
        width=30,
        fg_color="#333333",
        command=lambda n=name: execute_command(n)
    )
    small_btn.pack(side="left", padx=5, pady=10)

# address bar icon

for icon, name in address_bar_btns:
    btn = ctk.CTkButton(
        address_bar,
        text=icon,
        width=30,
        fg_color="transparent",
        hover_color="#333333",
        font=("Segoe UI Symbol", 18),
        command=lambda n=name: execute_command(n)
    )
    btn.pack(side='right', pady=5, padx=5)


show_page("Home")

root.mainloop()