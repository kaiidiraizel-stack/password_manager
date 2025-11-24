from cryptography.fernet import Fernet
import os

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        """Generates a new Fernet key and saves it to the specified file path."""
        self.key = Fernet.generate_key()
        try:
            with open(path, 'wb') as f:
                f.write(self.key)
            print(f"[SUCCESS] New key created and saved to {path}")
        except Exception as e:
            print(f"[ERROR] Could not save key: {e}")

    def load_key(self, path):
        """Loads an existing Fernet key from the specified file path."""
        try:
            with open(path, 'rb') as f:
                self.key = f.read()
            print(f"[SUCCESS] Key loaded from {path}")
        except FileNotFoundError:
            print(f"[ERROR] Key file not found at {path}")
        except Exception as e:
            print(f"[ERROR] Could not load key: {e}")

    def create_password_file(self, path, initial_values=None):
        """Sets the password file path and populates it with initial values."""
        if self.key is None:
            print("[ERROR] Cannot create password file: Key not loaded. Load or create a key first.")
            return

        self.password_file = path
        # Ensure the file is created empty or truncated before adding new data
        open(path, 'w').close() 

        if initial_values is not None:
            for site, password in initial_values.items():
                # We call the internal method to avoid recursive file opening
                self._add_to_file(site, password)
        
        print(f"[SUCCESS] Password file created at {path} with initial values.")


    def load_password_file(self, path):
        """Loads and decrypts all passwords from the specified file into the dictionary."""
        if self.key is None:
            print("[ERROR] Cannot load password file: Key not loaded. Load or create a key first.")
            return

        self.password_file = path
        self.password_dict = {}
        fernet_cipher = Fernet(self.key)
        
        try:
            with open(path, 'r') as f:
                for line in f:
                    if ":" not in line:
                        continue # Skip malformed lines
                    
                    # Split into site and encrypted text
                    site, encrypted_token = line.strip().split(":", 1)
                    
                    try:
                        
                        decrypted_password = fernet_cipher.decrypt(encrypted_token.encode()).decode()
                        self.password_dict[site] = decrypted_password
                    except Exception as e:
                        
                        print(f"[WARNING] Could not decrypt password for site '{site}'. Data might be corrupted or key is wrong. ({e})")
                        self.password_dict[site] = "[DECRYPTION FAILED]"
            
            print(f"[SUCCESS] Passwords loaded from {path}.")
            
        except FileNotFoundError:
            print(f"[ERROR] Password file not found at {path}")

    def _add_to_file(self, site, password):
        """Internal helper to encrypt and append a password to the file."""
        if self.key is None or self.password_file is None:
            print("[ERROR] Key or password file not set. Cannot save.")
            return

        try:
            encrypted = Fernet(self.key).encrypt(password.encode())
            with open(self.password_file, 'a') as f:
                f.write(site + ":" + encrypted.decode() + "\n")
            
        except Exception as e:
            print(f"[ERROR] Failed to write password for '{site}' to file: {e}")


    def add_password(self, site, password):
        """Adds a password to the dictionary and appends it to the file."""
        if self.key is None:
            print("[ERROR] Cannot add password: Key not loaded.")
            return
            
        self.password_dict[site] = password

        if self.password_file is not None:
            self._add_to_file(site, password)
            print(f"[SUCCESS] Added '{site}'.")
        else:
            print(f"[INFO] Added '{site}' to memory, but file not set (use option 3 or 4 to save persistently).")


    def get_password(self, site):
        """Retrieves the decrypted password from the dictionary."""
        if site in self.password_dict:
            return self.password_dict[site]
        else:
            return f"Site '{site}' not found in the vault."
    
def main():
    initial_passwords = {
        "email": "12345",
        "facebook": "myfacebook",
    }
    
    pm = PasswordManager()
    
    print("\n" + "="*40)
    print("      Simple Fernet Password Manager")
    print("="*40)
    print("""What do you want to do?
      (1) Create a NEW key (WARNING: Overwrites existing key)
      (2) Load an EXISTING key
      (3) Create NEW password file (WARNING: Overwrites existing file)
      (4) Load EXISTING password file
      (5) Add a new password
      (6) Get a password
      (q) Quit      
      """)

    done = False

    while not done:
        choice = input("Enter your choice: ").strip().lower()
        if choice == "1":
            path = input("Enter path to save the NEW key (e.g., mykey.key): ").strip()
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path to load the EXISTING key (e.g., mykey.key): ").strip()
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path to create NEW password file (e.g., passwords.txt): ").strip()
            pm.create_password_file(path, initial_passwords) 
        elif choice == "4":
            path = input("Enter path to load EXISTING password file (e.g., passwords.txt): ").strip()
            pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter the site/service name: ").strip()
            password = input("Enter the password: ").strip()
            pm.add_password(site, password)
        elif choice == "6":
            site = input("What site/service do you want the password for: ").strip()
            print(f"Password for {site} is: {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("Bye!")
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or q.")

if __name__ == "__main__":
    main()
