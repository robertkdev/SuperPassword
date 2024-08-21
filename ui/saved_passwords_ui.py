import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils.password_utils import copy_to_clipboard


class SavedPasswordsUI:
    def __init__(self, notebook, password_manager, create_regeneration_tab_callback):
        self.password_manager = password_manager
        self.create_regeneration_tab_callback = create_regeneration_tab_callback
        self.saved_frame = ttk.Frame(notebook, padding="20")
        notebook.add(self.saved_frame, text="Saved Passwords")

        self.saved_passwords_tree = ttk.Treeview(self.saved_frame, columns=('Name', 'Password'), show='headings', height=15)
        self.configure_treeview()
        self.create_buttons()
        self.update_saved_passwords_tree()

    def configure_treeview(self):
        self.saved_passwords_tree.heading('Name', text='Name')
        self.saved_passwords_tree.heading('Password', text='Password')
        self.saved_passwords_tree.column('Name', width=200)
        self.saved_passwords_tree.column('Password', width=350)
        self.saved_passwords_tree.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

    def create_buttons(self):
        saved_button_frame = ttk.Frame(self.saved_frame)
        saved_button_frame.pack(fill=tk.X)

        ttk.Button(saved_button_frame, text="Regenerate", command=self.regenerate_password).pack(side=tk.LEFT, padx=5, pady=10)
        ttk.Button(saved_button_frame, text="Delete", command=self.delete_saved_password).pack(side=tk.LEFT, padx=5, pady=10)
        ttk.Button(saved_button_frame, text="Copy Selected", command=self.copy_saved_to_clipboard).pack(side=tk.LEFT, padx=5, pady=10)
        
        # New button to save everything to a new file
        ttk.Button(saved_button_frame, text="Save All to File", command=self.save_all_to_file).pack(side=tk.LEFT, padx=5, pady=10)


    def regenerate_password(self):
        selected = self.saved_passwords_tree.selection()
        if selected:
            name = self.saved_passwords_tree.item(selected[0])['values'][0]
            self.create_regeneration_tab_callback(name)

    def delete_saved_password(self):
        selected = self.saved_passwords_tree.selection()
        if selected:
            name = self.saved_passwords_tree.item(selected[0])['values'][0]
            # Show a confirmation dialog
            confirm_delete = messagebox.askokcancel(
                "Delete Password",
                f"Are you sure you want to delete the saved password '{name}'?"
            )
            if confirm_delete:
                self.password_manager.delete_password(name)
                self.update_saved_passwords_tree()



    def copy_saved_to_clipboard(self):
        selected = self.saved_passwords_tree.selection()
        if selected:
            name = self.saved_passwords_tree.item(selected[0])['values'][0]
            copy_to_clipboard(self.password_manager.get_saved_passwords()[name]['password'])

    def update_saved_passwords_tree(self):
        for i in self.saved_passwords_tree.get_children():
            self.saved_passwords_tree.delete(i)
        for name, data in self.password_manager.get_saved_passwords().items():
            password = data['password']
            self.saved_passwords_tree.insert('', 'end', values=(name, password))

    def get_selected_password(self):
        selected = self.saved_passwords_tree.selection()
        if selected:
            item = self.saved_passwords_tree.item(selected[0])
            name = item['values'][0]
            return {'Name': name, 'Settings': self.password_manager.get_saved_passwords()[name]['settings']}
        return None

    def save_all_to_file(self):
        """Save all passwords to a new file."""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if save_path:
            self.password_manager.save_passwords_to_new_file(save_path)