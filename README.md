Super Password

A user-friendly password management application built with Python and Tkinter. This application allows you to generate, save, and manage passwords securely. It is designed to be simple yet powerful, ensuring that your passwords are always stored in a safe and accessible location.

Features
Password Generation: Generate secure passwords based on customizable criteria such as length, inclusion of uppercase/lowercase letters, digits, and symbols.
Save Passwords: Save generated passwords with custom names, allowing easy retrieval and management.
Password Regeneration: Easily regenerate a saved password with the same or updated settings.
Persistent Storage: Passwords are saved to a file in your home directory, ensuring consistency across application launches.
Manual File Saving: Save all passwords to a new file at any time, similar to saving in a different slot in a video game.
User-Friendly Interface: Simple and intuitive interface built with Tkinter, featuring tabbed navigation for generating and managing passwords.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/password-manager.git
cd password-manager
Install dependencies:
Ensure you have Python installed. Then, install the necessary dependencies using pip:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python main.py
Packaging as an executable (optional):
If you want to package the application as an executable using PyInstaller:

bash
Copy code
pyinstaller --onefile --windowed main.py
Usage
First Launch:

Upon launching the application for the first time, you will be prompted to select a file location where your passwords will be saved. This location will be remembered for future sessions.
The default save location is within the PasswordManager directory in your home directory.
Generating Passwords:

Use the "Generate Password" tab to create a new password. You can customize the password length and the types of characters included.
Once generated, the password can be copied to your clipboard or saved with a custom name.
Managing Saved Passwords:

View and manage your saved passwords in the "Saved Passwords" tab.
You can regenerate a password, delete it, or copy it to your clipboard.
Saving to a New File:

If you wish to save your passwords to a different file, use the "Save All to File" option in the "Saved Passwords" tab.
File Structure
bash
Copy code
password-manager/
│
├── main.py                 # Main entry point of the application
├── file_manager.py         # Handles file operations and path management
├── password_manager.py     # Manages passwords and interacts with the file manager
├── ui/
│   ├── password_generator_ui.py   # Handles the UI for generating passwords
│   ├── saved_passwords_ui.py      # Handles the UI for managing saved passwords
│   └── regeneration_ui.py         # Handles the UI for regenerating passwords
├── utils/
│   └── password_utils.py    # Utility functions for password generation and clipboard operations
└── README.md                # This README file
Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or new features you'd like to add.

License
This project is licensed under the MIT License.
