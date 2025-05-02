# 🎵 YouTube Music Folder Flattener

A lightweight desktop tool by **Neverklear Technologies** to recursively gather music files from subfolders and place them into a single destination folder — ideal for YouTube Music uploads or media organization.

---

### ✅ Features

- 🗂 Drag-and-drop folder support
- 📁 Select a parent folder to scan
- 🎯 Choose a destination folder
- 🎵 Supports `.mp3`, `.flac`, `.wav`, `.aac`, `.m4a`, `.ogg`
- ⏱ Real-time progress bar and estimated time remaining
- 📜 Logging to both the GUI and `log.txt`
- ⚙️ Auto-renames to avoid overwriting duplicates
- 🪟 Fully standalone `.exe` for Windows (no installation needed)
- 🧠 Built with Python, Tkinter, and PyInstaller

---

### 🖼 Screenshots

![image](https://github.com/user-attachments/assets/8bb577cd-8b5e-473b-834b-765f85dade1d)



---

### 🚀 How to Use

1. **Download the latest release `.exe`**
2. Launch the app (no installation required)
3. Drag a folder into the window or use **"Select Parent Folder"**
4. Select the **destination folder**
5. Click **Start Transfer** and watch it go!

---

### 🧰 For Developers

To build it from source:

```bash
pip install tkinterdnd2
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=logo.ico music_mover.py
