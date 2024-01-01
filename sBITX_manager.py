#!/usr/bin/env python3

"""
Remote application that interacts with the sBITX using telnet protocol.

Author: W9JES

License: MIT License

Copyright (c) 2023 J. Kujawa
"""



import tkinter as tk
from tkinter import simpledialog, messagebox
import telnetlib
import json
import time
import threading

class TelnetGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("sBITX Telnet Manager")
        self.master.geometry("250x350")  # Set width and height

        self.telnet_connection = None
        self.telnet_host = "sbitx.local"
        self.telnet_port = 8081

        self.command_buttons = []
        
        self.scan_running = False
        self.scan_thread = None
        self.scan_wait_time = 1  # Default wait time between commands in seconds

        # Load button configurations from a config file
        self.load_button_config()

        # Create menu
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        telnet_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Main", menu=telnet_menu)

        telnet_menu.add_command(label="Open Telnet", command=self.open_telnet)
        telnet_menu.add_command(label="Close Telnet", command=self.close_telnet)
        telnet_menu.add_command(label="About", command=self.show_about_dialog)

        command_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Command", menu=command_menu)
        command_menu.add_command(label="Add Frequency", command=self.add_command)
        command_menu.add_command(label="VFO A", command=lambda: self.send_command("vfo a"))
        command_menu.add_command(label="VFO B", command=lambda: self.send_command("vfo b"))
        command_menu.add_command(label="IF Level", command=lambda: self.show_input_dialog("IF"))
        command_menu.add_command(label="Bandwidth", command=lambda: self.show_input_dialog("Bandwidth"))
        command_menu.add_command(label="Audio Level", command=lambda: self.show_input_dialog("Audio"))
        command_menu.add_command(label="RF Output", command=lambda: self.show_input_dialog("RF Output"))
        command_menu.add_command(label="Clear Messages", command=lambda: self.send_command("clear"))
        
        agc_submenu = tk.Menu(command_menu, tearoff=0)
        command_menu.add_cascade(label="AGC", menu=agc_submenu)
        agc_submenu.add_command(label="Off", command=lambda: self.send_command("agc off"))
        agc_submenu.add_command(label="Slow", command=lambda: self.send_command("agc slow"))
        agc_submenu.add_command(label="Medium", command=lambda: self.send_command("agc medium"))
        agc_submenu.add_command(label="Fast", command=lambda: self.send_command("agc fast"))


        command_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mode", menu=command_menu)
        command_menu.add_command(label="LSB", command=lambda: self.send_command("m lsb"))
        command_menu.add_command(label="USB", command=lambda: self.send_command("m usb"))
        command_menu.add_command(label="CW", command=lambda: self.send_command("m cw"))
        command_menu.add_command(label="FT8", command=lambda: self.send_command("m ft8"))
        command_menu.add_command(label="Digital", command=lambda: self.send_command("m digital"))
        
        # Create a menu for the scan feature
        scan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Scan", menu=scan_menu)
        scan_menu.add_command(label="Start Scan", command=self.start_scan)
        scan_menu.add_command(label="Stop Scan", command=self.stop_scan)
        scan_menu.add_separator()
        scan_menu.add_command(label="Set Scan Wait Time", command=self.set_scan_wait_time)

        # Display existing buttons on the main screen
        self.update_main_screen()

    def open_telnet(self):
        try:
            self.telnet_connection = telnetlib.Telnet(self.telnet_host, self.telnet_port)
        except Exception as e:
            print(f"Error: {e}")

    def close_telnet(self):
        try:
            if self.telnet_connection:
                self.telnet_connection.close()
        except Exception as e:
            print(f"Error: {e}")
    
    def show_about_dialog(self):
        about_text = "sBITX Telnet Manager\n\nCreated by JJ-W9JES\nLicense: MIT License\nCopyright (c) 2024 J. Kujawa"
        messagebox.showinfo("About", about_text)

    def add_command(self):
        new_command = simpledialog.askstring("Add Command", "Enter the frequency:")
        if new_command:
            button_info = {'text': new_command}
            button = tk.Button(self.master, text=button_info['text'], command=lambda cmd=button_info['text']: self.send_command(cmd))
            button.bind("<Button-3>", lambda event, info=button_info: self.show_context_menu(event, info))
            button.pack()
            self.command_buttons.append(button_info)
            self.save_button_config()

    def show_input_dialog(self, command):
        user_input = simpledialog.askstring(f"Enter {command} Command", f"Enter the {command} command:")
        if user_input and command == "Bandwidth":
            user_input = "bw " + user_input
        if user_input and command == "IF":
            user_input = "if " + user_input
        if user_input and command == "RF Output":
            user_input = "drive " + user_input        
        if user_input and command == "Audio":
            user_input = "audio " + user_input         
        self.send_command(user_input)

    def send_command(self, command):
        try:
            if self.telnet_connection:
                self.telnet_connection.write(command.encode('ascii') + b'\r\n')
                response = self.telnet_connection.read_until(b'>', timeout=2).decode('ascii')
                print(f"Command '{command}' response: {response}")
        except Exception as e:
            print(f"Error: {e}")
            
    def send_freq_command(self, command):
        try:
            if self.telnet_connection:
                # Prepend "f " to the command before sending
                command_with_f = f'f {command}'
                self.telnet_connection.write(command_with_f.encode('ascii') + b'\r\n')
                response = self.telnet_connection.read_until(b'>', timeout=2).decode('ascii')
                print(f"Command '{command_with_f}' response: {response}")
        except Exception as e:
            print(f"Error: {e}")
  
    def show_context_menu(self, event, button_info):
        context_menu = tk.Menu(self.master, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda info=button_info: self.edit_command(info))
        context_menu.add_command(label="Remove", command=lambda info=button_info: self.remove_command(info))
        context_menu.post(event.x_root, event.y_root)

    def edit_command(self, button_info):
        new_command = simpledialog.askstring("Edit Command", "Edit the command:", initialvalue=button_info['text'])
        if new_command:
            button_info['text'] = new_command
            self.update_main_screen()
            self.save_button_config()

    def remove_command(self, button_info):
        confirmation = messagebox.askyesno("Remove Command", f"Are you sure you want to remove '{button_info['text']}'?")
        if confirmation:
            self.command_buttons.remove(button_info)
            self.update_main_screen()
            self.save_button_config()

    def update_main_screen(self):
        # Clear existing buttons
        for button in self.master.winfo_children():
            if isinstance(button, tk.Button):
                button.destroy()

        # Display updated buttons on the main screen
        for button_info in self.command_buttons:
            button = tk.Button(self.master, text=button_info['text'], command=lambda cmd=button_info['text']: self.send_freq_command(cmd))
            button.bind("<Button-3>", lambda event, info=button_info: self.show_context_menu(event, info))
            button.pack()

    def start_scan(self):
        if not self.scan_running:
            self.scan_running = True
            self.scan_thread = threading.Thread(target=self.scan_commands)
            self.scan_thread.start()

    def stop_scan(self):
        if self.scan_running:
            self.scan_running = False
            if self.scan_thread.is_alive():
                self.scan_thread.join()

    def scan_commands(self):
        while self.scan_running:
            for button_info in self.command_buttons:
                self.send_command(button_info['text'])
                time.sleep(self.scan_wait_time)

    def set_scan_wait_time(self):
        user_input = simpledialog.askfloat("Set Scan Wait Time", "Enter wait time between commands (seconds):", initialvalue=self.scan_wait_time)
        if user_input is not None:
            self.scan_wait_time = max(0, user_input)

        # You can also update the scan thread's sleep time if it's currently running
        if self.scan_running:
            self.stop_scan()
            self.start_scan()

        print(f"Scan wait time set to {self.scan_wait_time} seconds.")
 
    def load_button_config(self):
        try:
            with open("button_config.json", "r") as config_file:
                self.command_buttons = json.load(config_file)
        except FileNotFoundError:
            # If the config file doesn't exist, create an empty list
            self.command_buttons = []

    def save_button_config(self):
        with open("sbmanagerconfig.json", "w") as config_file:
            json.dump(self.command_buttons, config_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = TelnetGUI(root)
    root.mainloop()
