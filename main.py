import tkinter as tk
from ui.password_generator_ui import PasswordGeneratorUI

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorUI(root)
    root.mainloop()