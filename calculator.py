import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

def on_button_click(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(number))

def on_clear_click():
    entry.delete(0, tk.END)

def on_operator_click(operator):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + operator)

def on_equal_click():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

root = tk.Tk()
root.title("Owen Calculator")
root.geometry("400x500")

style = ThemedStyle(root)
style.set_theme("plastik")

entry = ttk.Entry(root, font=("Arial", 20))
entry.pack(pady=20)

button_frame = ttk.Frame(root)
button_frame.pack()

buttons = [
    ["7", "8", "9", "+"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "*"],
    ["0", ".", "=", "/"],
    ["sqrt", "pow", "sin", "cos"],
    ["tan", "log", "exp", "integral"]
]

for i in range(len(buttons)):
    for j in range(len(buttons[i])):
        if buttons[i][j] == "=":
            button = ttk.Button(button_frame, text=buttons[i][j], command=on_equal_click)
        else:
            button = ttk.Button(button_frame, text=buttons[i][j], command=lambda x=buttons[i][j]: on_button_click(x))
        button.grid(row=i, column=j, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="C", command=on_clear_click)
clear_button.grid(row=6, column=0, padx=5, pady=5)

root.mainloop()