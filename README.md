# 🔐 Simple Fernet Password Manager

This is a Python-based **command-line password manager** that uses the `cryptography` library's **Fernet** symmetric encryption to securely store site passwords in a local text file.

**⚠️ WARNING:** This tool's security relies entirely on the **secrecy and integrity of your encryption key file**. **Do not lose the key**, and **do not share it**. If the key is lost, your passwords are unrecoverable.

-----

## ✨ Features

  * **Key Management:** Generate and load a Fernet encryption key.
  * **Encrypted Storage:** Passwords are encrypted before being written to a file and decrypted only upon loading into memory.
  * **Simple CLI:** Easy-to-use command-line interface for common tasks.
  * **Persistent Storage:** Passwords are saved persistently to a specified file.

-----

## 💻 Prerequisites

You need **Python 3.x** installed on your system.

### Installation

This project requires the `cryptography` library. Install it using pip:

```bash
pip install cryptography
```

-----

## 🚀 How to Run

1.  Save the provided code as a Python file (e.g., `pass_manager.py`).

2.  Run the script from your terminal:

    ```bash
    python pass_manager.py
    ```

-----

## 🧭 Usage Workflow

The application is run interactively via the command line. You must follow these steps to use the password storage functionality:

### 1\. Key Management (Choose 1 or 2)

  * **Option (1) Create a NEW key:** Generates a new unique encryption key and saves it to a file (e.g., `mykey.key`). **You must back up this key securely.**
  * **Option (2) Load an EXISTING key:** Loads an existing key from a file. **You must load the correct key to decrypt your existing password file.**

### 2\. Password File Management (Choose 3 or 4)

  * **Option (3) Create NEW password file:** Sets the file path and creates a new, empty (or pre-populated) encrypted password file (e.g., `passwords.txt`). **⚠️ This will overwrite any existing file at the specified path.**
  * **Option (4) Load EXISTING password file:** Loads and decrypts all entries from an existing encrypted file into the program's memory.

### 3\. Core Operations (Choose 5 or 6)

  * **Option (5) Add a new password:** Prompts for the site and password, adds it to the in-memory vault, and encrypts/appends it to the currently set password file.
  * **Option (6) Get a password:** Retrieves the decrypted password for a specified site from the in-memory vault.

### 4\. Quit

  * **Option (q) Quit:** Exits the application.

-----

## 🔨 Code Structure

The core functionality is encapsulated in the `PasswordManager` class.

| Method | Description |
| :--- | :--- |
| `__init__` | Initializes the key, file path, and in-memory password dictionary. |
| `create_key(path)` | Generates a new Fernet key and saves it. |
| `load_key(path)` | Loads an existing Fernet key. |
| `create_password_file(path, initial_values)` | Sets the file path and creates a new encrypted file, optionally adding initial passwords. |
| `load_password_file(path)` | Loads all entries from the file, decrypts them using the loaded key, and stores them in `self.password_dict`. |
| `add_password(site, password)` | Adds a password to the in-memory dictionary and persists it to the encrypted file. |
| `get_password(site)` | Retrieves a decrypted password from the in-memory dictionary. |
| `_add_to_file(site, password)` | **Internal:** Encrypts and appends the password to the file. |
