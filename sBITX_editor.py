#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import json

class ReorderGUI:
    def __init__(self, master, items):
        self.master = master
        self.master.title("sBITX Manager Memory Editor")
        self.items = items

        self.listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, font=("Helvetica", 14, "bold"))
        self.listbox.pack(expand=True, fill=tk.BOTH)

        for item in self.items:
            self.listbox.insert(tk.END, item['text'])

        up_button = tk.Button(self.master, text="Up", command=self.move_up, font=("Helvetica", 14, "bold"))
        up_button.pack(side=tk.LEFT, padx=10)

        down_button = tk.Button(self.master, text="Down", command=self.move_down, font=("Helvetica", 14, "bold"))
        down_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(self.master, text="Save Order", command=self.save_order, font=("Helvetica", 14, "bold"))
        save_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(self.master, text="Exit", command=self.exit_application, font=("Helvetica", 14, "bold"))
        exit_button.pack(side=tk.LEFT, padx=10)

    def move_up(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] > 0:
            selected_index = int(selected_index[0])
            self.items[selected_index], self.items[selected_index - 1] = self.items[selected_index - 1], self.items[selected_index]
            self.update_listbox(selected_index - 1)

    def move_down(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] < len(self.items) - 1:
            selected_index = int(selected_index[0])
            self.items[selected_index], self.items[selected_index + 1] = self.items[selected_index + 1], self.items[selected_index]
            self.update_listbox(selected_index + 1)

    def update_listbox(self, new_index):
        self.listbox.delete(0, tk.END)
        for item in self.items:
            self.listbox.insert(tk.END, item['text'])
        self.listbox.selection_set(new_index)

    def save_order(self):
        try:
            with open("sbmanager_config.json", "w") as config_file:
                json.dump(self.items, config_file)
            messagebox.showinfo("Save Order", "Order saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save order: {e}")

    def exit_application(self):
        self.master.destroy()

if __name__ == "__main__":
    try:
        with open("sbmanager_config.json", "r") as config_file:
            items = json.load(config_file)
    except FileNotFoundError:
        items = []

    root = tk.Tk()
    reorder_app = ReorderGUI(root, items)
    root.mainloop()
