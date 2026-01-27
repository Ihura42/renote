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

SAVE_PATH = r"B:\python\ReNote\save"

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#main containers

sidebar = ctk.CTkFrame(root, width=60, fg_color=SIDEBAR_BG, corner_radius=0)
sidebar.pack(side='left', fill='y')

file_explorer = ctk.CTkFrame(root, width=200, fg_color=EXPLORER_BG, corner_radius=0)
file_explorer.pack(side='left', fill='y')

main = ctk.CTkFrame(root, fg_color=BG, corner_radius=0)
main.pack(side='right', fill='both', expand=True)


#showing main paig content

def show_page(page_name):
    for child in main.winfo_children():
        child.destroy()

    if page_name == 'Home':
        title = ctk.CTkEntry(main, font=("Segoe UI", 28, "bold"), width = 600, fg_color='transparent', border_width=0)
        title.insert("0", "Untitled")
        title.pack(pady=(50, 0), padx=(100,0), anchor="w")

        text_area = ctk.CTkTextbox(main, font=("Segoe UI", 16))
        text_area.insert("0.0", "New text...")
        text_area.pack(fill='both', expand=True, padx=100, side = 'top')
    else:
        lbl = ctk.CTkLabel(main, text=page_name, font=("Segoe UI", 32))
        lbl.pack(expand=True)

def execute_command(command):
    if command == 'New note':
        new_name = "newfile.txt"
        file_path = os.path.join(SAVE_PATH, new_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        refresh_files()
        open_file(new_name)   



def save_file(file_path, text_area):
    with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    current_content = text_area.get("1.0", 'end-1c') 

    if current_content == content:
        print("No changes detected...")
    else:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(current_content)
        print(f"Auto-saved: {file_path}")
    root.after(5000, save_file, file_path, text_area)

# opening file and showin gin main

def open_file(name):
    for child in main.winfo_children():
        child.destroy()

    title = ctk.CTkEntry(main, font=("Segoe UI", 28, "bold"), width = 600, fg_color='transparent', border_width=0)
    title.insert("0", name)
    title.pack(pady=(50, 0), padx=(100,0), anchor="w")


    file_path = os.path.join(SAVE_PATH, name)

    with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    text_area = ctk.CTkTextbox(main, font=("Segoe UI", 16))
    text_area.insert("0.0", content)
    text_area.pack(fill='both', expand=True, padx=100, side = 'top')

    
    root.after(5000, save_file, file_path, text_area)


# explorer container inside 

explorer_header = ctk.CTkFrame(file_explorer, fg_color="transparent")
explorer_header.pack(fill="x", side="top", padx=5, pady=5)

exporer_file_list = ctk.CTkFrame(file_explorer, fg_color=FILES_BG)
exporer_file_list.pack(fill = 'both', expand = True)

#lists of buttons(icons)

buttons = [
    ("⌂", "Home"), ("📄", "Notes"), ("⛓", "Links"),
    ("▦", "Grid"), ("📅", "Calendar"), ("📁", "Files"), (">", "Terminal"),
]

explorer_icons = [("📄+", "New note"),
                   ("📁+", "New folder")]

#importing files from folder

path = "B:\python\ReNote\save"
filter = ".txt"

files = []
def refresh_files():
    files.clear()
    
    for filename in os.listdir(SAVE_PATH):
        if filename.endswith(".txt"):
            files.append(filename)

    for child in exporer_file_list.winfo_children():
            child.destroy()

    for name in files:

        file_line = ctk.CTkButton(exporer_file_list, text = f"{ name }",anchor= 'w',hover_color="#333333", height=30 , fg_color = FILES_BG, cursor = 'hand2', command = lambda n=name:open_file(n))
        file_line.pack(side = 'top', pady = 5, padx = (10,70))
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






show_page("Home")

root.mainloop()