import ast
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import solve

def is_valid_entry(check):
    try:
        literal = eval(check)
    except Exception as e:
        return False

    check_1 = isinstance(literal, tuple)
    check_2 = all(isinstance(i, (int,int)) for i in literal)

    return check_1 and check_2

def save_to_file():
    val_1 = coord_1.get()
    val_2 = coord_2.get()
    val_3 = coord_3.get()
    val_4 = coord_4.get()
    val_5 = coord_5.get()
    values = [val_1, val_2, val_3, val_4, val_5]
    print(values)
    values = list(filter(bool, values))
    true_values = []
    check_3 = all(0 <= x <= 50 and 0 <= y <= 50 for (x, y) in true_values)
    if not check_3:
        tk.messagebox.showerror("Error", "Invalid entry")
        return
    for i in range(len(values)):
        if is_valid_entry(values[i]):
            true_values.append(values[i])
        else:
            tk.messagebox.showerror("Error", "Invalid entry")
            return
    if true_values:
        existing = []
        with open("recent_vals.txt", "r+") as file:
            for x in range(4):
                line = file.readline()
                if not line:
                    break
                existing.append(line)

        with open("recent_vals.txt", "w+") as updated_file:
            existing.insert(0, str(true_values))
            for item in existing:
                updated_file.write(item.strip() + "\n")

        print(f"true_values: {true_values}")
        true_values = list(map(eval, true_values))
        solve.solve_app(true_values)
    else:
        tk.messagebox.showerror("Error", "No values present")


def clicked_recent_button(button_num):
    converted = [ast.literal_eval(s) for s in ast.literal_eval(button_num)]
    solve.solve_app(converted)


root = tk.Tk()
root.title("Pathfinder")
root.geometry("300x400")
tabs = ttk.Notebook(root)

tab_1 = tk.Frame(tabs)
tab_2 = tk.Frame(tabs)
tabs.add(tab_1, text="Entries")
tabs.add(tab_2, text="Load Entries")
tabs.grid(row=0, column=0, sticky="nsew")

labels = [1, 2, 3, 4, 5]
for i in range(len(labels)):
    label = ttk.Label(tab_1, text=f"Coordinates {labels[i]}", font=("Arial", 15))
    label.grid(column=0, row=i)

coord_1 = ttk.Entry(tab_1)
coord_1.grid(column=1, row=0)
coord_2 = ttk.Entry(tab_1)
coord_2.grid(column=1, row=1)
coord_3 = ttk.Entry(tab_1)
coord_3.grid(column=1, row=2)
coord_4 = ttk.Entry(tab_1)
coord_4.grid(column=1, row=3)
coord_5 = ttk.Entry(tab_1)
coord_5.grid(column=1, row=4)

submit_button = ttk.Button(tab_1, text="Submit", command=save_to_file)
submit_button.grid(column=1, row=5)

scroll_bar = scrolledtext.ScrolledText(tab_1,  width=30, height=15, wrap=tk.WORD, font=("Arial", 12))
scroll_bar.grid(column=0, row=6, columnspan=2)
info = ""
info += "Enter coordinates in the following format (x, y)\n"
info += "Coordinates must be between 0<=x<50 and 0<=y<50\n"
info += "Draw barriers by holding down left click\n"
info += "Press c to clear barriers\n"
info += "Press s to solve\n"

scroll_bar.insert(tk.INSERT, info)
scroll_bar.config(state=tk.DISABLED)

# tab 2 (load from recent)
recent_button_data = []
lines = []
with open("recent_vals.txt", "r") as file:
    for i in range(5):
        line = file.readline()
        line.strip()
        if not line:
            break
        lines.append(line)

button_1 = ttk.Button(tab_2, text=lines[0], command=lambda: clicked_recent_button(lines[0]))
button_1.grid(row=0, column=0, ipadx=100, ipady=19)
button_2 = ttk.Button(tab_2, text=lines[1], command=lambda: clicked_recent_button(lines[1]))
button_2.grid(row=1, column=0, ipadx=100, ipady=19)
button_3 = ttk.Button(tab_2, text=lines[2], command=lambda: clicked_recent_button(lines[2]))
button_3.grid(row=2, column=0, ipadx=100, ipady=19,)
button_4 = ttk.Button(tab_2, text=lines[3], command=lambda: clicked_recent_button(lines[3]))
button_4.grid(row=3, column=0, ipadx=100, ipady=19)
button_5 = ttk.Button(tab_2, text=lines[4], command=lambda: clicked_recent_button(lines[4]))
button_5.grid(row=4, column=0, ipadx=100, ipady=19)

root.mainloop()
