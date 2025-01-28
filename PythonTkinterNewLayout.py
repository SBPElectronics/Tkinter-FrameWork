import csv # Library
import os # Library
from tkinter import Tk, Frame, Menu, Label, Button, Toplevel, Entry, PhotoImage # Library
from tkinter import messagebox, filedialog # Library
import hashlib # Library
import sqlite3 # Library
import requests # Library
import shutil # Library
import sys # Library
import subprocess # Library
from PIL import Image, ImageTk # Library
import tkinter as tk # Library


class TkinterFrame(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.initUI() # Calls main screen

    def initUI(self):
        # Clear all widgets before adding new UI elements
        for widget in self.master.winfo_children():
            if not isinstance(widget, Menu):  # Keep the menu bar intact
                widget.destroy() # Destroys the window before it

        # Main content for the app
        Label(self.master, text="Tkinter Base Layout", font=("Arial", 20)).pack() # Application name
        canvas = tk.Canvas(self.master, height=2, width=400, bg="black", highlightthickness=0) # Draws a line between the two labels for a neat look
        canvas.pack(pady=5, fill = "x") # The placing
        Label(self.master, text="Current Available Accounts:", font=("Sans Serif ", 15)).pack()

        self.master.geometry("350x400")  # Set the desired width x height
        self.master.title("Simple Menu") # Window Name

        # File path for options.csv
        file_path = "options.csv" # Looks options.csv, if not there it creates it, if it is there then it skips this [art]
        if not os.path.exists(file_path): # If it doesn't exists
            with open(file_path, "w", encoding="utf-8") as f: # Creates the file
                f.write("Name,Path\n")  # Write the column in the options.csv

        # Read paths from options.csv
        self.display_paths() # Displays the paths
 
        menubar = Menu(self.master) # Creates the toolbar at the top
        self.master.config(menu=menubar) 

        # File menu
        fileMenu = Menu(menubar, tearoff=0) 
        fileMenu.add_command(label="New", command=self.create_account_screen) # New button
        fileMenu.add_command(label="Open", command=self.open_account) # Open button
        menubar.add_cascade(label="File", menu=fileMenu) # File dropdown

        # Help menu
        helpMenu = Menu(menubar, tearoff=0)
        helpMenu.add_command(label="About", command=self.onAbout) # About button
        helpMenu.add_command(label="Check For Updates", command=self.onCheckForUpdates) # Check for Updates Button
        menubar.add_cascade(label="Help", menu=helpMenu) # Help dropdown

        # Create a frame for the footer and place it at the bottom
        footer_frame = Frame(self.master, bg="black", height=40)
        footer_frame.pack(side="bottom", fill="x") # Puts the footer at the bottom

        # Add a label to the footer frame
        footer_label = Label(footer_frame, text="15/01/24", fg="white", bg="black") 
        footer_label.pack(side = "left") # Puts the writing on the left

        footer_label = Label(footer_frame, text="Layout Version 1", fg="white", bg="black") 
        footer_label.pack(side = "right") # Puts the writing on the right

    def display_paths(self):
        """Display file paths from options.csv with validation and removal options."""
        file_path = "options.csv" # 
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))  # Read all rows at once

            if len(rows) > 1:  # Ensure there's at least a header and one entry
                header = rows[0]  # Save the header
                entries = rows[1:]  # Exclude the header
                unique_entries = []  # To store unique rows
                seen = set()  # To track seen (name, path) pairs

                # Create a frame for displaying buttons and labels
                frame = Frame(self.master)
                frame.pack(fill='both', expand=True, pady=10)

                # Clear any existing widgets in the frame (if needed)
                for widget in frame.winfo_children():
                    widget.destroy()

                for index, row in enumerate(entries):
                    if row:  # Ensure the row is not empty
                        name_path = row[0] # Verify name row
                        folder_path = row[1] # Verify folder row
                        identifier = (name_path, folder_path)  # Puts them in a variable.


                        if identifier not in seen: # Checks if they are there
                            seen.add(identifier) 
                            unique_entries.append(row)

                            # Check if the folder exists
                            exists = os.path.exists(folder_path)

                            # Create a label for each entry with color indication
                            lbl = Label(frame, text=name_path, fg="black" if exists else "red", font=("Arial", 10))
                            lbl.grid(row=index, column=0, padx=5, pady=5, sticky="w")

                            # If valid, add an "Open" button next to the name
                            if exists:
                                btn_open = Button(
                                    frame,
                                    text="Open",
                                    command=lambda path=folder_path: self.open_folder()
                                )
                                btn_open.grid(row=index, column=1, padx=5, pady=5)

                            # Add a "Remove" button for invalid paths
                            if not exists:
                                btn_remove = Button(
                                    frame,
                                    text="Remove",
                                    command=lambda path=folder_path: self.remove_entry(path)
                                )
                                btn_remove.grid(row=index, column=1, padx=5, pady=5)

                

                # Rewrite the file with only unique entries
                with open(file_path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)  # Write the header
                    writer.writerows(unique_entries)  # Write unique entries

                
                    
            else:
                messagebox.showinfo("Info", "No entries to display in the file.")
        except FileNotFoundError:
            messagebox.showinfo("Error", f"{file_path} not found.")
            self.initUI()


    def remove_entry(self, folder_path):
        """Remove an entry from options.csv and refresh the display."""
        file_path = "options.csv"
        try:
            # Read all rows in the CSV file
            with open(file_path, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))  # Read all rows at once

            header = rows[0]  # Save the header
            entries = [row for row in rows[1:] if row and row[1] != folder_path]  # Exclude the entry to be removed

            # Rewrite the CSV file without the removed entry
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)  # Write the header
                writer.writerows(entries)  # Write the remaining entries

            # Notify user of successful removal
            messagebox.showinfo("Success", f"Entry {folder_path} removed successfully.")

            # Refresh the display by calling display_paths() again
            self.initUI()

        except FileNotFoundError:
            messagebox.showinfo("Error", f"{file_path} not found.")




    def open_folder(self):
        """Open the manage_account_screen"""
        self.manage_account()

    def manage_account(self):
        '''The Manage Account Screen'''
        for widget in self.master.winfo_children():
            if not isinstance(widget, Menu):  # Keep the menu bar intact
                widget.destroy()

        self.master.geometry("450x300")  # Set the desired width x height

        Label(self.master, text="Welcome", font=("Arial", 12)).pack(fill = "x") 
        Button(self.master, text="Back", command=self.initUI).pack(fill="y")

    def open_account(self):
        """Open an account by selecting a folder."""
        folder_selected = filedialog.askopenfilename( 
            title="Select Folder",
            initialdir="/",
            filetypes=[("Database Files", "*.db"), ("CSV Files", "*.csv") , ("Text Files", "*.txt")] # Sets what files can be opened
        )

        if folder_selected:
            # Extract the file name and path
            file_name = os.path.basename(folder_selected)
            file_path = os.path.dirname(folder_selected)

            # Check if the selected folder is already in options.csv
            try:
                with open("options.csv", "r", encoding="utf-8") as f:
                    existing_entries = [
                        row[1] for row in csv.reader(f) if len(row) > 1
                    ]

                if folder_selected in existing_entries:
                    messagebox.showinfo("Already Exists", "The selected folder is already in the list.")
                    return
            except FileNotFoundError:
                # If options.csv doesn't exist, treat it as no existing entries
                existing_entries = []

            # Add the folder to the CSV if it's not already there
            with open("options.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([file_name, folder_selected])

            messagebox.showinfo("Account Opened", f"Selected folder: {folder_selected}")
            self.display_paths()  # Refresh to only show the last path
            self.initUI()
        else:
            messagebox.showwarning("No Selection", "No folder was selected.")


    def create_account_screen(self):
        """Create account screen is here"""
        # Clear current content and show the new account creation UI
        for widget in self.master.winfo_children():
            if not isinstance(widget, Menu):  # Keep the menu bar intact
                widget.destroy()

        self.master.geometry("300x350")  # Set the desired width x height

        # New account form
        Label(self.master, text="Create New Account", font=("Arial", 14)).pack(fill='both', expand=True)

        # Account name entry
        Label(self.master, text="Account Name", font=("Arial", 12)).pack(fill='both', expand=True)
        account_name_entry = Entry(self.master)
        account_name_entry.pack(fill='both', padx=10, pady=10)

        # Password entry
        Label(self.master, text="Password", font=("Arial", 12)).pack(fill='both', expand=True)
        password_entry = Entry(self.master, show="*")
        password_entry.pack(fill='both', padx=10, pady=10)

        # Confirm password entry
        Label(self.master, text="Confirm Password", font=("Arial", 12)).pack(fill='both', expand=True)
        confirm_password_entry = Entry(self.master, show="*")
        confirm_password_entry.pack(fill='both', padx=10, pady=10)

        # Submit button to create account
        Button(self.master, text="Select Location and Create Account", command=lambda: self.create_account(
            account_name_entry.get(),
            password_entry.get(),
            confirm_password_entry.get()
        )).pack(fill='both', pady=10, padx=10)

        # Button to go back to the main UI
        Button(self.master, text="Go Back", command=self.initUI).pack(fill='both', pady=10, padx=10)

    def create_account(self, account_name, password, confirm_password):
        """Handle account creation logic"""
        if not account_name or not password:
            messagebox.showerror("Error", "Username or password cannot be empty.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Ask the user to select a folder for the database
        folder_selected = filedialog.askdirectory(title="Select Folder", initialdir="/")
        if not folder_selected:
            messagebox.showerror("Error", "You must select a folder.")
            return

        path = os.path.join(folder_selected, f'{account_name}.db')
        if os.path.exists(path):
            messagebox.showwarning("Warning", "Database already exists.")
            return

        password_file_path = f"{path}.csv"

        # Write the account information to the options.csv file
        with open("options.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([account_name, f"{folder_selected}/{account_name}.db"])

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, folder TEXT NOT NULL)''')

        with open(password_file_path, "w", encoding="utf-8") as f:
            f.write(hashed_password)  # Write the hashed password to a file

        try:
            c.execute('INSERT INTO users (username, password, folder) VALUES (?, ?, ?)', (account_name, "password not here", folder_selected))
            conn.commit()
            messagebox.showinfo("Success", f"Account created successfully.\nDatabase saved to: {path}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            conn.close()
            self.initUI()  # Go back to the main UI

    

    def onAbout(self):
        """Display about information."""
        new_window = Toplevel(self.master)
        new_window.title("About")
        new_window.geometry("300x300")
        new_window.resizable(True, False)

        # Path to the image
        image_path = os.path.join(os.path.dirname(__file__), "Logo.png")

        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"The image file '{image_path}' does not exist.")

            # Open and resize the image using Pillow
            img = Image.open(image_path)
            img = img.resize((150, 150))  # Resize to 150x150 pixels (adjust as needed)

            # Convert to Tkinter-compatible PhotoImage
            self.image = ImageTk.PhotoImage(img)

            image_label = Label(new_window, image=self.image)
            image_label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            return  # Stop further execution

        Label(new_window, text="Made in 2025", font=("Arial", 10)).pack(fill="both", pady=5)
        Label(new_window, text="https://www.youtube.com/@SBPElectronics", font=("Arial", 10)).pack(fill="both", pady=5)

    def onCheckForUpdates(self):
        """Check for updates by comparing the current version with the searched version using GitHub API and OAuth token."""
        new_window = Toplevel(self.master)
        new_window.title("Check For Updates")
        new_window.geometry("300x200")
        new_window.resizable(False, False)

        current_version = '1'  # Current version of your application (as a string)
        
        
        # GitHub API URL for fetching the file content
        api_url = 'https://api.github.com/repos/{YOUR_ACCOUNT_NAME}/{REPO}/contents/{LINK_TO_FIND_THE_VERSION_NUMBER}'
        
        # Personal Access Token for authentication
        token = 'github_pat_{FINISH_TOKEN}'

        try:
            # Add token to headers for authentication
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3.raw'  # Request raw file content
            }

            # Send a GET request to fetch the file content
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                # The file content is directly returned as text
                file_content = response.text.strip()

                # Extract version information from the file content
                if file_content.startswith("Tk Frame - v."):
                    searched_version = file_content.split('.')[-1].strip()  # Extract the numeric part of the version
                else:
                    raise ValueError("Invalid file format.")

                # Compare versions numerically
                if int(searched_version) > int(current_version):
                    message = (f"A new version is available!\n"
                            f"Current Version: v.{current_version}\n"
                            f"Latest Version: v.{searched_version}") 
                    Label(new_window, text=message, font=("Arial", 12), wraplength=280, justify="center").pack(pady=20)
                    Button(new_window, text="Click To Update", command=self.download_and_updating_exe).pack(pady=10)
                else:
                    message = f"Your application is up-to-date.\nCurrent Version: v.{current_version}"
                    Label(new_window, text=message, font=("Arial", 12), wraplength=280, justify="center").pack(pady=20)

            else:
                raise Exception(f"Failed to fetch the file. Status code: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking for updates:\n{e}")

    def download_and_updating_exe(self):
        """Trigger the updater .exe."""
        updater_exe_path = "updater.exe"  # Path to the updater .exe
        exe_download_url = "https://github.com/{YOUR_ACCOUNT_NAME}/{YOUR_REPO}/raw/main/{ZIP_LOCTION_ON_GITHUB}"
        current_exe_path = os.path.abspath(sys.argv[0])  # Path to the running .exe

        try:
            # Check if the updater .exe exists
            if not os.path.exists(updater_exe_path):
                raise FileNotFoundError(f"Updater .exe '{updater_exe_path}' not found.")

            # Launch the updater with necessary arguments
            subprocess.Popen(
                [updater_exe_path, exe_download_url, current_exe_path],
                shell=False
            )

            # Exit the main application
            messagebox.showinfo("Update Started", "The application will now close for the update.")
            self.master.quit()
        except Exception as e:
            messagebox.showerror("Update Error", f"Failed to launch the updater: {e}")


def main():
    root = Tk()  # Use Tk class here
    root.geometry("250x150+300+300")
    app = TkinterFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
