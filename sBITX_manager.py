#!/usr/bin/env python3

"""
Remote application that interacts with the sBITX using telnet protocol.

Author: W9JES

License: MIT License

Copyright (c) 2023 J. Kujawa
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, font, scrolledtext
import tkinter.simpledialog
import telnetlib
import json
import time
import threading
import socket
import webbrowser

class FrequencyInputDialog(tk.Toplevel):
    def __init__(self, parent, title, initial_values=None):
        super().__init__(parent)
        self.title(title)

        self.freq_var = tk.StringVar()
        self.mode_var = tk.StringVar()
        self.bw_var = tk.StringVar()
        self.if_var = tk.StringVar()
        self.agc_var = tk.StringVar()

        if initial_values:
            self.freq_var.set(initial_values.get('text', ''))
            self.mode_var.set(initial_values.get('mode', ''))
            self.bw_var.set(initial_values.get('bandwidth', ''))
            self.if_var.set(initial_values.get('if_setting', ''))
            self.agc_var.set(initial_values.get('agc_setting', ''))

        font_style = font.Font(family="Helvetica", size=14, weight="bold")

        tk.Label(self, text="Frequency:", font=font_style).grid(row=0, column=0, sticky=tk.E)
        ttk.Entry(self, textvariable=self.freq_var, font=font_style).grid(row=0, column=1, columnspan=2, sticky=tk.W)

        tk.Label(self, text="Mode:", font=font_style).grid(row=1, column=0, sticky=tk.E)
        Mode_options = ["LSB", "USB", "CW", "CWR", "FT8", "PSK", "RTTY", "Digital", "2Tone"]
        ttk.Combobox(self, textvariable=self.mode_var, values=Mode_options, font=font_style).grid(row=1, column=1, columnspan=2, sticky=tk.W)

        tk.Label(self, text="Bandwidth:", font=font_style).grid(row=2, column=0, sticky=tk.E)
        ttk.Entry(self, textvariable=self.bw_var, font=font_style).grid(row=2, column=1, columnspan=2, sticky=tk.W)

        tk.Label(self, text="IF:", font=font_style).grid(row=3, column=0, sticky=tk.E)
        ttk.Entry(self, textvariable=self.if_var, font=font_style).grid(row=3, column=1, columnspan=2, sticky=tk.W)

        tk.Label(self, text="AGC:", font=font_style).grid(row=4, column=0, sticky=tk.E)
        AGC_options = ["Off", "Slow", "Med", "Fast"]
        ttk.Combobox(self, textvariable=self.agc_var, values=AGC_options, font=font_style).grid(row=4, column=1, columnspan=2, sticky=tk.W)

        tk.Button(self, text="OK", command=self.ok_button_click, font=font_style).grid(row=5, column=0, columnspan=3, pady=10, padx=10)

    def ok_button_click(self):
        self.destroy()

class MessageWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Decoded Messages")

        self.response_text = tk.Text(self, wrap=tk.WORD, height=10, width=50, font=("Helvetica", 14, "bold"))
        self.response_text.pack(expand=True, fill=tk.BOTH)

        button_frame = tk.Frame(self)
        button_frame.pack()

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_text, font=("Helvetica", 14, "bold"))
        clear_button.pack(side=tk.LEFT)

        increase_font_button = tk.Button(button_frame, text="Larger Text", command=self.increase_font_size, font=("Helvetica", 14, "bold"))
        increase_font_button.pack(side=tk.LEFT)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def append_response(self, response):
        # Remove curly braces from the response
        response = response.replace("{", "").replace("}", "")

        self.response_text.insert(tk.END, response + '')
        self.response_text.see(tk.END)

    def clear_text(self):
        self.response_text.delete(1.0, tk.END)

    def on_close(self):
        self.withdraw()

    def increase_font_size(self):
        # Increase the font size of the response_text widget
        current_font = self.response_text.cget("font")
        current_size = int(current_font.split(" ")[1])
        new_size = current_size + 2  # You can adjust the increment value

        self.response_text.config(font=("Helvetica", new_size, "bold"))

class TelnetGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("sBITX Telnet Manager")

        # Font configuration
        self.available_font_sizes = [14, 16, 18, 20, 22, 24, 26, 28, 30]  # Add more sizes as needed
        self.current_font_size_index = 0

        self.telnet_connection = None
        self.telnet_host = "sbitx.local"
        self.telnet_port = 8081

        self.command_buttons = []

        self.scan_running = False
        self.scan_thread = None
        self.scan_wait_time = 5  # Default wait time between commands in seconds

        self.load_button_config()

        self.message_window = MessageWindow(master)
        self.message_window.withdraw()

        threading.Thread(target=self.check_responses).start()

        menubar = tk.Menu(master, font=("Helvetica", 14, "bold"))
        master.config(menu=menubar)

        telnet_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 14, "bold"))
        menubar.add_cascade(label="Main", menu=telnet_menu)

        telnet_menu.add_command(label="Open Telnet", command=self.open_telnet)
        telnet_menu.add_command(label="Close Telnet", command=self.close_telnet)
        telnet_menu.add_separator()
        telnet_menu.add_command(label="Larger Text", command=self.increase_font_size)
        telnet_menu.add_command(label="About", command=self.show_about_dialog)
        telnet_menu.add_command(label="Exit", command=self.exit_application)

        command_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 14, "bold"))
        menubar.add_cascade(label="Command", menu=command_menu)
        frequency_submenu = tk.Menu(command_menu, tearoff=0)
        frequency_submenu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="Frequency", menu=frequency_submenu)
        frequency_submenu.add_command(label="Add", command=self.add_command_submenu)
        frequency_submenu.add_command(label="Edit", command=self.edit_command_submenu)
        frequency_submenu.add_command(label="Remove", command=self.remove_command_submenu)

        command_menu.add_command(label="IF Level", command=lambda: self.show_input_dialog("IF"))
        command_menu.add_command(label="Bandwidth", command=lambda: self.show_input_dialog("Bandwidth"))
        command_menu.add_command(label="Audio Level", command=lambda: self.show_input_dialog("Audio"))
        command_menu.add_command(label="RF Output", command=lambda: self.show_input_dialog("RF Output"))
        command_menu.add_command(label="TX Compressor", command=lambda: self.show_input_dialog("Comp Lvl"))
        command_menu.add_command(label="Clear sBitx Messages", command=lambda: self.send_command("clear"))
        command_menu.add_command(label="Decode Messages", command=self.open_response_box)
        command_menu.add_command(label="Open sBitx Web", command=self.open_web_browser)

        vfo_submenu = tk.Menu(command_menu, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="VFO", menu=vfo_submenu)
        vfo_submenu.add_command(label="VFO A", command=lambda: self.send_command("vfo a"))
        vfo_submenu.add_command(label="VFO B", command=lambda: self.send_command("vfo b"))

        agc_submenu = tk.Menu(command_menu, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="AGC", menu=agc_submenu)
        agc_submenu.add_command(label="Off", command=lambda: self.send_command("agc off"))
        agc_submenu.add_command(label="Slow", command=lambda: self.send_command("agc slow"))
        agc_submenu.add_command(label="Medium", command=lambda: self.send_command("agc med"))
        agc_submenu.add_command(label="Fast", command=lambda: self.send_command("agc fast"))

        step_submenu = tk.Menu(command_menu, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="Step", menu=step_submenu)
        step_submenu.add_command(label="10H", command=lambda: self.send_command("step 10h"))
        step_submenu.add_command(label="100H", command=lambda: self.send_command("step 100h"))
        step_submenu.add_command(label="1K", command=lambda: self.send_command("step 1k"))
        step_submenu.add_command(label="10K", command=lambda: self.send_command("step 10k"))

        rit_submenu = tk.Menu(command_menu, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="RIT", menu=rit_submenu)
        rit_submenu.add_command(label="On", command=lambda: self.send_command("rit on"))
        rit_submenu.add_command(label="Off", command=lambda: self.send_command("rit off"))

        splitx_submenu = tk.Menu(command_menu, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="Split", menu=splitx_submenu)
        splitx_submenu.add_command(label="On", command=lambda: self.send_command("split on"))
        splitx_submenu.add_command(label="Off", command=lambda: self.send_command("split off"))

        span_submenu = tk.Menu(command_menu, tearoff=0, font=("Helvetica", 14, "bold"))
        command_menu.add_cascade(label="WF Span", menu=span_submenu)
        span_submenu.add_command(label="2.5K", command=lambda: self.send_command("span 2.5k"))
        span_submenu.add_command(label="6K", command=lambda: self.send_command("span 6k"))
        span_submenu.add_command(label="10K", command=lambda: self.send_command("span 10k"))
        span_submenu.add_command(label="25K", command=lambda: self.send_command("span 25k"))

        command_menu = tk.Menu(menubar, tearoff=0)
        command_menu.configure(font=('Helvetica', 14, 'bold'))
        menubar.add_cascade(label="Mode", menu=command_menu)
        command_menu.add_command(label="LSB", command=lambda: self.send_command("m lsb"))
        command_menu.add_command(label="USB", command=lambda: self.send_command("m usb"))
        command_menu.add_command(label="CW", command=lambda: self.send_command("m cw"))
        command_menu.add_command(label="CW Reverse", command=lambda: self.send_command("m cwr"))
        command_menu.add_command(label="FT8", command=lambda: self.send_command("m ft8"))
        command_menu.add_command(label="RTTY", command=lambda: self.send_command("m rtty"))
        command_menu.add_command(label="PSK31", command=lambda: self.send_command("m psk31"))
        command_menu.add_command(label="Digital", command=lambda: self.send_command("m digital"))
        command_menu.add_command(label="2Tone", command=lambda: self.send_command("m 2tone"))

        scan_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 14, "bold"))
        menubar.add_cascade(label="Scan", menu=scan_menu)
        scan_menu.add_command(label="Start Scan", command=self.start_scan)
        scan_menu.add_command(label="Stop Scan", command=self.stop_scan)
        scan_menu.add_separator()
        scan_menu.add_command(label="Set Scan Wait Time", command=self.set_scan_wait_time)
        
        self.listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, font=("Helvetica", self.available_font_sizes[self.current_font_size_index], "bold"))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.config(width=39, height=30)  # Adjust the value according to your needs
        self.scrollbar = tk.Scrollbar(self.master, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<ButtonRelease-1>", self.on_listbox_click)
        self.update_main_screen()

    def check_responses(self):
        try:
            while True:
                if self.telnet_connection:
                    response = self.telnet_connection.read_until(b'>', timeout=0.1).decode('ascii')
                    if response:
                        # Append response to the message window
                        self.message_window.append_response(response)
                else:
                    # Telnet connection is closed, break the loop
                    break
        except Exception as e:
            print(f"Error in response polling: {e}")

    def open_response_box(self):
        self.message_window.deiconify()

    def open_telnet(self):
        try:
            if not self.telnet_connection:
                self.telnet_connection = telnetlib.Telnet(self.telnet_host, self.telnet_port)
                response = self.telnet_connection.read_until(b'>', timeout=1).decode('ascii')
                messagebox.showinfo("Telnet", "Telnet connection opened successfully.")

                # Start the response polling thread after opening the telnet connection
                threading.Thread(target=self.check_responses).start()

        except socket.error as e:
            messagebox.showerror("Telnet Error", "Invalid response. The SBITX transceiver should be restarted.")

    def close_telnet(self):
        try:
            if self.telnet_connection:
                self.telnet_connection.close()
                self.telnet_connection = None
                messagebox.showinfo("Telnet", "Telnet connection closed successfully.")
            else:
                messagebox.showinfo("Telnet", "No Telnet connection to close.")
        except Exception as e:
            messagebox.showerror("Telnet Error", f"Error closing Telnet connection: {e}")

    def show_about_dialog(self):
        about_text = """
        sBITX Telnet Manager v2.0

        Created by W9JES

        License: MIT License

        Copyright (c) 2024 J. Kujawa

        www.w9jes.com

        https://github.com/drexjj/sBITX-Manager
        """

        about_window = tk.Toplevel(self.master)
        about_window.title("About")

        about_label = tk.Label(about_window, text=about_text, justify=tk.LEFT, padx=10, pady=10)
        about_label.config(font=("TkDefaultFont", 11, "bold"))  # Adjust the font size as needed
        about_label.pack()

    def on_listbox_click(self, event):
        selected_index = self.listbox.nearest(event.y)

        if selected_index >= 0 and selected_index < len(self.command_buttons):
            selected_command = self.command_buttons[selected_index]['text']
            self.send_freq_command(selected_command)

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
        if user_input and command == "Comp Lvl":
            user_input = "comp " + user_input

        self.send_command(user_input)

    def send_command(self, command):
        try:
            if self.telnet_connection:
                self.telnet_connection.write(command.encode('ascii') + b'\r\n')
                response = self.telnet_connection.read_until(b'>', timeout=0.1).decode('ascii')
                print(f"Command '{command}' response: {response}")
        except socket.error as e:
            messagebox.showerror("Error", f"Failed to send command '{command}': {e}")

    def send_freq_command(self, command):
        try:
            if self.telnet_connection:
                button_info = next(info for info in self.command_buttons if info['text'] == command)
                frequency = button_info['text']
                mode = button_info['mode']
                bandwidth = button_info['bandwidth']
                if_setting = button_info.get('if_setting', '')
                agc_setting = button_info.get('agc_setting', '')

                commands = [
                    f'f {frequency}',
                    f'm {mode}',
                    f'bw {bandwidth}',
                    f'if {if_setting}',
                    f'agc {agc_setting}',
                    'clear'
                ]

                for cmd in commands:
                    self.telnet_connection.write(cmd.encode('ascii') + b'\r\n')
                    response = self.telnet_connection.read_until(b'>', timeout=0.1).decode('ascii')
                    print(f"Command '{cmd}' response: {response}")

        except Exception as e:
            print(f"Error: {e}")

    def add_command_submenu(self):
        dialog = FrequencyInputDialog(self.master, "Add Frequency")

        self.master.wait_window(dialog)

        new_frequency = dialog.freq_var.get()
        new_mode = dialog.mode_var.get()
        new_bandwidth = dialog.bw_var.get()
        new_if_setting = dialog.if_var.get()
        new_agc_setting = dialog.agc_var.get()

        if new_frequency and new_mode and new_bandwidth:
            button_info = {'text': new_frequency, 'mode': new_mode, 'bandwidth': new_bandwidth,
                           'if_setting': new_if_setting, 'agc_setting': new_agc_setting}

            item_text = f"{button_info['text']} | M: {button_info['mode']} | BW: {button_info['bandwidth']} | IF: {button_info['if_setting']} | A: {button_info['agc_setting']}"
            self.listbox.insert(tk.END, item_text)

            self.command_buttons.append(button_info)
            self.save_button_config()

    def edit_command_submenu(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            selected_info = self.command_buttons[selected_index]

            dialog = FrequencyInputDialog(self.master, "Edit Frequency", initial_values=selected_info)

            self.master.wait_window(dialog)

            edited_frequency = dialog.freq_var.get()
            edited_mode = dialog.mode_var.get()
            edited_bandwidth = dialog.bw_var.get()
            edited_if_setting = dialog.if_var.get()
            edited_agc_setting = dialog.agc_var.get()

            if edited_frequency and edited_mode and edited_bandwidth:
                selected_info['text'] = edited_frequency
                selected_info['mode'] = edited_mode
                selected_info['bandwidth'] = edited_bandwidth
                selected_info['if_setting'] = edited_if_setting
                selected_info['agc_setting'] = edited_agc_setting

                self.update_main_screen()
                self.save_button_config()

    def remove_command_submenu(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            self.listbox.delete(selected_index)
            removed_info = self.command_buttons.pop(selected_index)
            self.save_button_config()

            print(f"Removed: {removed_info}")

    def show_context_menu(self, event, button_info):
        context_menu = tk.Menu(self.master, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda info=button_info: self.edit_command(info))
        context_menu.add_command(label="Remove", command=lambda info=button_info: self.remove_command(info))
        context_menu.post(event.x_root, event.y_root)

    def update_main_screen(self):
        self.listbox.delete(0, tk.END)

        for button_info in self.command_buttons:
            item_text = f" {button_info['text']} | {button_info['mode']} | BW: {button_info['bandwidth']} | IF: {button_info['if_setting']} | AGC: {button_info['agc_setting']}"
            self.listbox.insert(tk.END, item_text)

    def increase_font_size(self):
        self.current_font_size_index = (self.current_font_size_index + 1) % len(self.available_font_sizes)
        self.listbox.config(font=("Helvetica", self.available_font_sizes[self.current_font_size_index], "bold"))
		
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
                self.send_freq_command(button_info['text'])
                time.sleep(self.scan_wait_time)

                # Check if scan_running is still True; if not, break out of the loop
                if not self.scan_running:
                    break

    def set_scan_wait_time(self):
        user_input = simpledialog.askfloat("Set Scan Wait Time", "Enter wait time between change (seconds):", initialvalue=self.scan_wait_time)
        if user_input is not None:
            self.scan_wait_time = max(0, user_input)

        if self.scan_running:
            self.stop_scan()
            self.start_scan()

        print(f"Scan wait time set to {self.scan_wait_time} seconds.")

    def open_web_browser(self):
        url = "http://sbitx.local:8080"
        webbrowser.open(url)

    def load_button_config(self):
        try:
            with open("sbmanager_config.json", "r") as config_file:
                self.command_buttons = json.load(config_file)
        except FileNotFoundError:
            self.command_buttons = []

    def save_button_config(self):
        with open("sbmanager_config.json", "w") as config_file:
            json.dump(self.command_buttons, config_file)

    def exit_application(self):
        confirmation = messagebox.askokcancel("Exit Application", "Are you sure you want to exit?")
        if confirmation:
            if self.telnet_connection:
                self.telnet_connection.close()
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TelnetGUI(root)
    root.mainloop()
