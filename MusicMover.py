import os
import shutil
import time
import threading
import sys
import tempfile
from tkinter import Button, Label, Text, END, filedialog, ttk, Scrollbar, RIGHT, Y
from tkinterdnd2 import TkinterDnD, DND_FILES

# Supported music extensions
MUSIC_EXTENSIONS = {".mp3", ".flac", ".wav", ".m4a", ".aac", ".ogg"}

class MusicMover:
    def __init__(self, root):
        self.root = root
        self.root.title("Music File Collector")
        self.root.geometry("600x400")

        # Load icon (works in PyInstaller EXE and raw script)
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'logo.ico')
            else:
                icon_path = 'logo.ico'
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")

        # Enable drag-and-drop for the entire window
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        self.source_folder = ""
        self.destination_folder = ""

        # Buttons
        Button(root, text="Select Parent Folder", command=self.select_source).pack(pady=5)
        Button(root, text="Select Destination Folder", command=self.select_destination).pack(pady=5)
        Button(root, text="Start Transfer", command=self.start_transfer).pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        # Logging to file
        self.log_file = open("log.txt", "w", encoding="utf-8")

        # Output log window
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.log = Text(root, height=15, width=70, yscrollcommand=scrollbar.set)
        self.log.pack(padx=10)
        scrollbar.config(command=self.log.yview)

    def handle_drop(self, event):
        folder_path = event.data.strip("{").strip("}")
        if os.path.isdir(folder_path):
            self.source_folder = folder_path
            self.log_output(f"Dropped source folder: {self.source_folder}")
        else:
            self.log_output("Please drop a valid folder.")

    def select_source(self):
        self.source_folder = filedialog.askdirectory(title="Select Parent Folder")
        self.log_output(f"Selected source: {self.source_folder}")

    def select_destination(self):
        self.destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        self.log_output(f"Selected destination: {self.destination_folder}")

    def start_transfer(self):
        if not self.source_folder or not self.destination_folder:
            self.log_output("Both folders must be selected before starting.")
            return

        thread = threading.Thread(target=self.copy_music_files)
        thread.start()

    def copy_music_files(self):
        start_time = time.time()
        music_files = []

        # Step 1: Gather all music files
        for dirpath, _, filenames in os.walk(self.source_folder):
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in MUSIC_EXTENSIONS:
                    music_files.append(os.path.join(dirpath, filename))

        total_files = len(music_files)
        self.progress["maximum"] = total_files
        self.log_output(f"Found {total_files} music files.")

        if total_files == 0:
            return

        # Step 2: Copy files with progress
        for idx, file_path in enumerate(music_files, start=1):
            try:
                base_name = os.path.basename(file_path)
                dest_path = os.path.join(self.destination_folder, base_name)

                # Avoid overwriting existing files
                counter = 1
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(base_name)
                    dest_path = os.path.join(self.destination_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy2(file_path, dest_path)
                elapsed = time.time() - start_time
                rate = elapsed / idx
                eta = rate * (total_files - idx)

                self.log_output(f"Copied: {file_path} → {dest_path} | ETA: {int(eta)}s")
                self.progress["value"] = idx
                self.root.update_idletasks()

            except Exception as e:
                self.log_output(f"Error copying {file_path}: {e}")

        self.log_output("Transfer complete!")
        self.log_file.write("\n--- Transfer Complete ---\n")
        self.log_file.close()

    def log_output(self, message):
        self.log.insert(END, message + "\n")
        self.log.see(END)
        self.log_file.write(message + "\n")
        self.log_file.flush()


# Run the GUI
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MusicMover(root)
    root.mainloop()
