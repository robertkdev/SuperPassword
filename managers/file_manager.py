import json
import os
from tkinter import filedialog, messagebox

class FileManager:
    def __init__(self, default_filename="saved_passwords.json"):
        self.filepath = self.get_saved_filepath() or self.ask_for_filepath(default_filename)

    def ask_for_filepath(self, default_filename):
        filepath = filedialog.asksaveasfilename(
            title="Select Save File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            self.save_filepath(filepath)
        return filepath or default_filename

    def get_saved_filepath(self):
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                return config.get("save_file")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_filepath(self, filepath):
        with open("config.json", "w") as config_file:
            json.dump({"save_file": filepath}, config_file)

    def save_data(self, data):
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Failed to load the save file.")
        return {}
