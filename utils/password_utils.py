import secrets
import string
import pyperclip
from tkinter import messagebox

def generate_password(settings):
    """Generate a password based on the provided settings."""
    length = settings['length']
    char_sets = []
    
    if settings['uppercase']:
        char_sets.append(string.ascii_uppercase)
    if settings['lowercase']:
        char_sets.append(string.ascii_lowercase)
    if settings['digits']:
        char_sets.append(string.digits)
    if settings['symbols']:
        char_sets.append(string.punctuation)
    
    if not char_sets:
        messagebox.showerror("Error", "Please select at least one character type.")
        return None
    
    # Combine all characters into one list for random selection
    all_chars = ''.join(char_sets)
    
    # Ensure at least one character from each selected set
    password_chars = [secrets.choice(charset) for charset in char_sets]
    
    # Add random characters to meet the required length
    password_chars.extend(secrets.choice(all_chars) for _ in range(length - len(password_chars)))
    
    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)

def copy_to_clipboard(password):
    """Copy the generated password to the system clipboard."""
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password generated yet.")
