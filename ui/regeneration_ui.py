import tkinter as tk
from tkinter import ttk
from utils.password_utils import generate_password

class RegenerationUI:
    def __init__(self, notebook, tab_name, password_data=None, regenerate_callback=None, update_display_callback=None, save_callback=None, copy_callback=None, close_callback=None):
        self.frame = ttk.Frame(notebook, padding="20")
        notebook.add(self.frame, text=tab_name)

        self.password_var = tk.StringVar()
        self.password_display = self.create_password_display()

        self.length_var, self.include_var = self.create_password_options(password_data)

        self.create_buttons(tab_name, regenerate_callback, save_callback, copy_callback)

        self.close_callback = close_callback

        if update_display_callback:
            self.password_var.trace("w", lambda *args: update_display_callback(self.password_var, self.password_display))

    def create_password_display(self):
        password_display = tk.Text(self.frame, height=2, wrap="word", font=("Helvetica", 16), state="disabled", borderwidth=2, relief="solid")
        password_display.pack(fill=tk.X, pady=(10, 20))
        return password_display

    def create_password_options(self, password_data):
        length_var = tk.IntVar(value=12 if not password_data else password_data['length'])
        length_frame = ttk.Frame(self.frame)
        length_frame.pack(fill=tk.X)

        ttk.Label(length_frame, text="Password Length:", anchor="w").pack(side=tk.LEFT, pady=5)
        ttk.Scale(length_frame, from_=8, to=64, orient='horizontal', variable=length_var, length=250, command=lambda value: length_var.set(round(float(value)))).pack(side=tk.LEFT, padx=(10, 0), pady=5)
        ttk.Label(length_frame, textvariable=length_var, width=3).pack(side=tk.LEFT, pady=5)

        include_var = {
            'uppercase': tk.BooleanVar(value=True if not password_data else password_data['uppercase']),
            'lowercase': tk.BooleanVar(value=True if not password_data else password_data['lowercase']),
            'digits': tk.BooleanVar(value=True if not password_data else password_data['digits']),
            'symbols': tk.BooleanVar(value=True if not password_data else password_data['symbols'])
        }

        options_frame = ttk.LabelFrame(self.frame, text="Character Options", padding=(10, 5))
        options_frame.pack(fill=tk.X, pady=10)

        for key, var in include_var.items():
            ttk.Checkbutton(options_frame, text=key.capitalize(), variable=var).pack(anchor="w")

        return length_var, include_var

    def create_buttons(self, tab_name, regenerate_callback, save_callback, copy_callback):
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Generate Password", command=lambda: self.update_password()).pack(side=tk.LEFT, padx=5, pady=10)
        
        if tab_name == "Generate Password":
            ttk.Button(button_frame, text="Copy to Clipboard", command=lambda: copy_callback(self.password_var.get())).pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Button(button_frame, text="Save Password", command=lambda: save_callback(self.password_var.get(), self.length_var, self.include_var)).pack(side=tk.LEFT, padx=5, pady=10)
        else:
            ttk.Button(button_frame, text="Save", command=lambda: self.save_regenerated_password(regenerate_callback)).pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Button(button_frame, text="Cancel", command=lambda: self.cancel_tab()).pack(side=tk.LEFT, padx=5, pady=10)

    def update_password(self):
        settings = {
            'length': self.length_var.get(),
            'uppercase': self.include_var['uppercase'].get(),
            'lowercase': self.include_var['lowercase'].get(),
            'digits': self.include_var['digits'].get(),
            'symbols': self.include_var['symbols'].get()
        }
        password = generate_password(settings)
        if password:
            self.password_var.set(password)

    def save_regenerated_password(self, regenerate_callback):
        regenerate_callback(self.password_var.get(), {
            'length': self.length_var.get(),
            'uppercase': self.include_var['uppercase'].get(),
            'lowercase': self.include_var['lowercase'].get(),
            'digits': self.include_var['digits'].get(),
            'symbols': self.include_var['symbols'].get()
        })
        self.close_tab()

    def cancel_tab(self):
        self.close_tab()

    def close_tab(self):
        if self.close_callback:
            self.close_callback()