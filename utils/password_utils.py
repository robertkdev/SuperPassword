import secrets
import string
import pyperclip
from tkinter import messagebox

import string
import secrets
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
    
    # Enforce minimum requirement of one character from each selected set
    password_chars = [secrets.choice(charset) for charset in char_sets]
    
    # Add random characters to meet the required length
    all_chars = ''.join(char_sets)
    password_chars.extend(secrets.choice(all_chars) for _ in range(length - len(password_chars)))
    
    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password_chars)
    
    # Ensure the password meets complexity requirements
    while not meets_complexity_requirements(password_chars, settings):
        password_chars = [secrets.choice(all_chars) for _ in range(length)]
        secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)

def meets_complexity_requirements(password_chars, settings):
    """Check if the password meets complexity requirements."""
    has_uppercase = any(char in string.ascii_uppercase for char in password_chars) if settings['uppercase'] else True
    has_lowercase = any(char in string.ascii_lowercase for char in password_chars) if settings['lowercase'] else True
    has_digit = any(char in string.digits for char in password_chars) if settings['digits'] else True
    has_symbol = any(char in string.punctuation for char in password_chars) if settings['symbols'] else True
    
    # Check for repeated characters (optional, to enhance security)
    no_repeats = len(set(password_chars)) == len(password_chars)
    
    # Check for consecutive characters (optional, to enhance security)
    no_consecutive = all(ord(password_chars[i]) - ord(password_chars[i-1]) != 1 
                         for i in range(1, len(password_chars)))
    
    return all([has_uppercase, has_lowercase, has_digit, has_symbol, no_repeats, no_consecutive])

def copy_to_clipboard(password):
    """Copy the generated password to the system clipboard."""
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password generated yet.")
