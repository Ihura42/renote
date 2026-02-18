import customtkinter as ctk
from pathlib import Path
import os

ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title('Renote')
root.geometry("1100x700")

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


#showing main paig content

def show_page(page_name):
    global current_page
    current_page = page_name

    for child in main_content.winfo_children():
        child.destroy()

    if page_name == 'Home':
        title = ctk.CTkEntry(main_content, font=("Segoe UI", 28, "bold"), width = 600, fg_color='transparent', border_width=0)
        title.insert("0", "Untitled")
        title.pack(pady=(50, 0), padx=(100,0), anchor="w")

        text_area = ctk.CTkTextbox(main_content, font=("Segoe UI", 16))
        text_area.insert("0.0", "New text...")
        text_area.pack(fill='both', expand=True, padx=100, side = 'top')
    elif page_name == 'Tags':
        tags_title = ctk.CTkTextbox(main_content, font=("Segoe UI", 28, "bold"), width = 600, fg_color='transparent', border_width=0)
        tags_title.insert("0", "Tags")
        tags_title.pack(pady=(50, 0), padx=(100,0), anchor="w")

        text_area = ctk.CTkTextbox(main_content, font=("Segoe UI", 16))
        text_area.insert("0.0", "There will be tags")
        text_area.pack(fill='both', expand=True, padx=100, side = 'top')
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


    if command == 'Save file' and current_file_path:
        save_file(current_file_path, current_text_area, current_title)


# save file
def save_file(file_path, text_area, title):
    if not file_path:
        return

    current_filename = title.get().strip()
    current_content = text_area.get("1.0", 'end-1c')

    filename = os.path.basename(file_path).replace(".md", "")

    if current_filename != filename:
        new_path = os.path.join(SAVE_PATH, current_filename + ".md")
        os.rename(file_path, new_path)
        file_path = new_path
        print(f"Renamed to: {new_path}")

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(current_content)

    print(f"Auto-saved: {file_path}")

    root.after(5000, save_file, file_path, text_area, title)


# opening file and showin gin main

def open_file(name):
    global current_file_path, current_text_area, current_title
    for child in main_content.winfo_children():
        child.destroy()

    title = ctk.CTkEntry(main_content, font=("Segoe UI", 28, "bold"), width = 600, fg_color='transparent', border_width=0)
    title.insert("0", name.replace(".md", ""))

    title.pack(pady=(50, 0), padx=(100,0), anchor="w")


    file_path = os.path.join(SAVE_PATH, name)

    with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    text_area = ctk.CTkTextbox(main_content, font=("Segoe UI", 16))
    text_area.insert("0.0", content)
    text_area.pack(fill='both', expand=True, padx=100, side = 'top')


    current_file_path = file_path
    current_text_area = text_area
    current_title = title

    root.after(5000, save_file, file_path, text_area, title)

# delete files
    
def delete_file(name):
    os.remove(SAVE_PATH + '/' + name)
    refresh_files()

def create_todolist():
    if current_text_area:
        current_text_area.insert("insert", "- [ ] New Task\n")


# explorer container inside 

explorer_header = ctk.CTkFrame(file_explorer, fg_color="transparent")
explorer_header.pack(fill="x", side="top", padx=5, pady=5)

exporer_file_list = ctk.CTkFrame(file_explorer, fg_color=FILES_BG)
exporer_file_list.pack(fill = 'both', expand = True)

#lists of buttons(icons)

buttons = [
    ("⌂", "Home"), ("📄", "Notes"), ("⛓", "Tags"),
]

explorer_icons = [("📄+", "New note"),
                   ("📁+", "New folder")]

address_bar_btns = [('💾', "Save file"),
                    ("☑", 'New todo list')]

#importing files from folder

files = []
def refresh_files():
    files.clear()
    
    for filename in os.listdir(SAVE_PATH):
        if filename.endswith(".md"):
            files.append(filename)

    for child in exporer_file_list.winfo_children():
            child.destroy()

    for name in files:

        file_placer = ctk.CTkFrame(exporer_file_list, fg_color=FILES_BG)
        file_placer.pack(fill = 'y')
        file_line = ctk.CTkButton(file_placer, text = f"{ name }",
                                anchor= 'w',hover_color="#333333",
                                height=30 ,
                                fg_color = FILES_BG,
                                cursor = 'hand2',
                                command = lambda n=name:open_file(n))
        file_line.pack(side = 'left', pady = 5, padx = 10)

        delete_button = ctk.CTkButton(file_placer, text = "x",
                                     hover_color = "#353535",
                                      fg_color = '#424242',
                                      width = 30,
                                      cursor = 'hand2',
                                      command = lambda n = name: delete_file(n))
        delete_button.pack(side=  'left', padx = (0, 20))
refresh_files()


#adding icons(buttons) to sidebar

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
    btn.pack(side = 'right', pady=5, padx=5)


show_page("Home")

root.mainloop()