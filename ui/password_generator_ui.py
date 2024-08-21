import tkinter as tk
from tkinter import ttk
from managers.password_manager import PasswordManager
from ui.regeneration_ui import RegenerationUI
from ui.saved_passwords_ui import SavedPasswordsUI
from utils.password_utils import generate_password, copy_to_clipboard

class PasswordGeneratorUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        
        # Set window dimensions
        window_width = 600
        window_height = 500

        # Get the screen's width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calculate position x and y coordinates to center the window
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Set the window size and position
        master.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        master.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.password_manager = PasswordManager(update_callback=self.update_saved_passwords_tree)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_tabs()

    def configure_styles(self):
        self.style.configure("TLabel", font=("Helvetica, 12"))
        self.style.configure("TButton", font=("Helvetica, 12"), padding=6, relief="flat")
        self.style.configure("TScale", font=("Helvetica, 10"))
        self.style.configure("TCheckbutton", font=("Helvetica, 11"))
        self.style.configure("TFrame", background="#f0f0f0")

    def create_tabs(self):
        self.gen_frame = self.create_password_generation_tab("Generate Password")
        self.saved_passwords_ui = SavedPasswordsUI(self.notebook, self.password_manager, self.regenerate_password)

    def create_password_generation_tab(self, tab_name, password_data=None, regenerate_callback=None):
        return RegenerationUI(
            self.notebook, tab_name, password_data, regenerate_callback,
            self.update_password_display, self.save_password, copy_to_clipboard,
            close_callback=self.close_regeneration_tab
        )

    def update_password_display(self, password_var, password_display):
        password_display.configure(state="normal")
        password_display.delete(1.0, tk.END)
        password_display.insert(tk.END, password_var.get())
        password_display.configure(state="disabled")

    def save_password(self, password, length_var, include_var):
        if password:
            settings = {
                'length': length_var.get(),
                'uppercase': include_var['uppercase'].get(),
                'lowercase': include_var['lowercase'].get(),
                'digits': include_var['digits'].get(),
                'symbols': include_var['symbols'].get()
            }
            self.password_manager.save_password(password, settings)
            self.update_saved_passwords_tree()

    def create_regeneration_tab(self, name):
        saved_settings = self.password_manager.get_saved_passwords()[name]['settings']
        new_tab = self.create_password_generation_tab(
            f"Regenerate '{name}'",
            password_data=saved_settings,
            regenerate_callback=lambda p, s: self.password_manager.regenerate_password(name, p, s)
        )
        self.notebook.select(self.notebook.tabs()[-1])
        self.disable_other_tabs()

    def disable_other_tabs(self):
        """Disable all tabs except the last one."""
        for i in range(len(self.notebook.tabs()) - 1):
            self.notebook.tab(i, state="disabled")

    def enable_all_tabs(self):
        """Enable all tabs."""
        for i in range(len(self.notebook.tabs())):
            self.notebook.tab(i, state="normal")

    def close_regeneration_tab(self):
        """Close the current tab and return to the saved passwords tab."""
        self.notebook.forget(self.notebook.select())
        self.enable_all_tabs()
        self.notebook.select(1)  # Assumes the saved passwords tab is the second one

    def update_saved_passwords_tree(self):
        self.saved_passwords_ui.update_saved_passwords_tree()

    def regenerate_password(self, name):
        settings = self.password_manager.get_saved_passwords()[name]['settings']
        use_previous = tk.messagebox.askyesno(
            "Regenerate Password",
            "Do you want to use the same settings as last time?"
        )

        if use_previous:
            new_password = generate_password(settings)
            if new_password:
                self.password_manager.regenerate_password(name, new_password, settings)
                self.update_saved_passwords_tree()
        else:
            self.create_regeneration_tab(name)