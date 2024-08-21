import json
import os
import sys
from tkinter import messagebox, simpledialog

class PasswordManager:
    def __init__(self, filename="saved_passwords.json", update_callback=None):
        # Determine if running as a PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        bundled_filepath = os.path.join(base_path, filename)
        self.user_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

        # Ensure the JSON file is initialized properly
        if not os.path.exists(self.user_filepath):
            if os.path.exists(bundled_filepath):
                with open(bundled_filepath, 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
                with open(self.user_filepath, 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                # If the file doesn't exist in either place, create an empty one
                with open(self.user_filepath, 'w') as f:
                    json.dump({}, f, indent=4)

        self.filepath = self.user_filepath
        self.saved_passwords = self.load_saved_passwords()
        self.update_callback = update_callback


    def load_saved_passwords(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    # If the file is empty or invalid, initialize it with an empty dictionary
                    data = {}
                for name, value in data.items():
                    if isinstance(value, str):
                        data[name] = {'password': value, 'settings': {}}
                return data
        return {}


    def save_passwords_to_file(self):
        with open(self.filepath, "w") as file:
            json.dump(self.saved_passwords, file, indent=4)
        if self.update_callback:
            self.update_callback()

    def save_password(self, password, settings):
        if password:
            name = simpledialog.askstring("Save Password", "Enter a name for this password:")
            if name:
                if name in self.saved_passwords:
                    # Prompt the user for confirmation to override
                    should_override = messagebox.askyesno(
                        "Override Password",
                        f"A password with the name '{name}' already exists. Do you want to override it?"
                    )
                    if not should_override:
                        return  # Do not save the password if the user doesn't want to override
                self.saved_passwords[name] = {'password': password, 'settings': settings}
                self.save_passwords_to_file()
                messagebox.showinfo("Success", f"Password saved as '{name}'")
        else:
            messagebox.showerror("Error", "No password generated to save.")

    def regenerate_password(self, name, new_password, settings):
        if new_password:
            self.saved_passwords[name] = {'password': new_password, 'settings': settings}
            self.save_passwords_to_file()
            messagebox.showinfo("Success", f"Password for '{name}' regenerated.")

    def delete_password(self, name):
        del self.saved_passwords[name]
        self.save_passwords_to_file()
        messagebox.showinfo("Success", f"Password for '{name}' deleted.")

    def get_saved_passwords(self):
        return self.saved_passwords

    def save_passwords_to_new_file(self, save_path):
        """Save the current saved passwords to a new file."""
        with open(save_path, "w") as file:
            json.dump(self.saved_passwords, file, indent=4)
        messagebox.showinfo("Success", f"Passwords saved to '{save_path}'")