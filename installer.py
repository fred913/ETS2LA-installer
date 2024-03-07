# Path: installer.py
#region Global variables
DEFAULT_INSTALL_LOCATION = r"C:/LaneAssist"
DEFAULT_SERVER = "github"
SERVERS = {
    "github": "https://github.com/Tumppi066/Euro-Truck-Simulator-2-Lane-Assist",
    "sourceforge": "https://sourceforge.net/projects/eurotrucksimulator2-laneassist/"
}
BRANCHES = {
    "main": "main",
    "development": "development"
}
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 250
PYTHON_VERSIONS = ["3.11", "3.10"]
PASTEL_GREEN = "#aaffa8"
PASTEL_RED = "#ff8a8a"
PASTEL_YELLOW = "#fffb8a"
GIT_DOWNLOAD_URL = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe"
PYTHON_DOWNLOAD_URL = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
OPEN_PYTHON_INSTALLER = False
OPEN_GIT_INSTALLER = False
#endregion
#region Imports
import tkinter as tk
from tkinter import ttk
import sv_ttk as sv
import os
import sys
import time
#endregion
#region Tkinter init
root = tk.Tk()
root.configure(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
root.pack_propagate(False)
root.grid_propagate(False)
root.title("Lane Assist Installer")
#endregion
#region Functions

def colorTitleBar():
    from ctypes import windll, c_int, byref, sizeof
    HWND = windll.user32.GetParent(root.winfo_id())
    returnCode = windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x1c1c1c)), sizeof(c_int))

def emptyLine(frame, size=12):
    ttk.Label(frame, text="", font=("Segoe UI", size)).pack()

#endregion
#region Pages
class CheckGitPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text="Checking for git", font=("Segoe UI", 16))
        self.label.pack()
        emptyLine(self, 16)
        self.checkGit()
    def checkGit(self):
        import subprocess
        try:
            subprocess.run(["git", "--version"])
            self.label.config(text="Git found", foreground=PASTEL_GREEN)
            self.button = ttk.Button(self, text="Next", command=self.next, width=30)
            self.button.pack(side="bottom")
        except FileNotFoundError:
            self.label.config(text="Git not found", foreground=PASTEL_RED)
            self.installButton = ttk.Button(self, text="Install", command=self.installGit, width=30)
            self.installButton.pack(pady=10)
            self.button = ttk.Button(self, text="Exit", command=sys.exit, width=30)
            self.button.pack(side="bottom")
    def installGit(self):
        import requests
        filename = GIT_DOWNLOAD_URL.split("/")[-1]
        # Streaming, so we can iterate over the response.
        response = requests.get(GIT_DOWNLOAD_URL, stream=True)

        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        lastUpdate = time.time()
        downloaded_size = 0
        with open(filename, "wb") as file:
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded_size += len(data)
                percentage = (downloaded_size / total_size) * 100
                print(f"Downloaded: {downloaded_size}/{total_size} bytes ({percentage:.2f}%)               ", end="\r")
                if time.time() - lastUpdate > 0.1:
                    self.installButton.config(text=f"Downloading {percentage:.2f}%", state="disabled")
                    self.master.update()
                    self.update()
                    lastUpdate = time.time()

        self.installButton.config(text="Installing", state="disabled")
        self.master.update()
        self.update()
        from tkinter import messagebox
        messagebox.showinfo("Git installer", "The installer will now open. You can use the default settings. After the installation is complete, click check.")
        # Run the installer silently
        os.startfile(filename)
        self.installButton.config(text="Check", command=self.reopen, state="normal")
        
    def reopen(self):
        self.pack_forget()
        next_page()
        
    def next(self):
        global CURRENT_PAGE
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class CheckPythonPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure()
        self.label = ttk.Label(self, text="Checking for Python", font=("Segoe UI", 16))
        self.label.pack(anchor="center", side="top")
        emptyLine(self, 16)
        self.checkPython()
    def checkPython(self):
        import subprocess
        try:
            version = subprocess.run(["python", "--version"], capture_output=True, text=True).stdout.replace("\n", "")
            found = False
            for v in PYTHON_VERSIONS:
                if v in version:
                    found = True
            
            if found:
                self.label.config(text=f"Python found ({version})", foreground=PASTEL_GREEN)
                self.button = ttk.Button(self, text="Next", command=self.next, width=30)
                self.button.pack(side="bottom")
            else:
                self.label.config(text="Python found, but wrong version", foreground=PASTEL_YELLOW)
                self.openWebsiteButton = ttk.Button(self, text="Open download website", command=self.openWebsite, width=30)
                self.openWebsiteButton.pack()
                self.button = ttk.Button(self, text="Exit", command=sys.exit, width=30)
                self.button.pack(side="bottom", pady=10)
        except FileNotFoundError:
            self.label.config(text="Python not found", foreground=PASTEL_RED)
            self.installButton = ttk.Button(self, text="Install", command=self.installPython, width=30)
            self.installButton.pack()
            self.button = ttk.Button(self, text="Exit", command=sys.exit, width=30)
            self.button.pack(side="bottom", pady=10)
    def openWebsite(self):
        import webbrowser
        webbrowser.open("https://wiki.tumppi066.fi/tutorials/installation/#step-1-download-python-and-git")      
        
    def installPython(self):
        import requests
        filename = PYTHON_DOWNLOAD_URL.split("/")[-1]
        # Streaming, so we can iterate over the response.
        response = requests.get(PYTHON_DOWNLOAD_URL, stream=True)

        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        lastUpdate = time.time()
        downloaded_size = 0
        with open(filename, "wb") as file:
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded_size += len(data)
                percentage = (downloaded_size / total_size) * 100
                print(f"Downloaded: {downloaded_size}/{total_size} bytes ({percentage:.2f}%)               ", end="\r")
                if time.time() - lastUpdate > 0.1:
                    self.installButton.config(text=f"Downloading {percentage:.2f}%", state="disabled")
                    self.master.update()
                    self.update()
                    lastUpdate = time.time()

        self.installButton.config(text="Installing", state="disabled")
        self.master.update()
        self.update()
        from tkinter import messagebox
        messagebox.showinfo("Python installer", "The installer will now open. You can use the default settings. After the installation is complete, click check.")
        # Run the installer silently
        os.startfile(filename)
        self.installButton.config(text="Check", command=self.reopen, state="normal")
          
    def next(self):
        global CURRENT_PAGE
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class LocationPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text="Install location", font=("Segoe UI", 16))
        self.label.pack()
        emptyLine(self, 16)
        self.button = ttk.Button(self, text="Next", command=self.next, width=30)
        self.button.pack(side="bottom", pady=10)
        self.entry = ttk.Entry(self, width=50)
        self.entry.pack(side="left")
        self.entry.insert(0, DEFAULT_INSTALL_LOCATION)
        self.getPathButton = ttk.Button(self, text="...", command=self.getPath)
        self.getPathButton.pack(side="right")
    def getPath(self):
        from tkinter import filedialog
        self.entry.delete(0, tk.END)
        self.entry.insert(0, filedialog.askdirectory())
    def next(self):
        global install_location
        global CURRENT_PAGE
        install_location = self.entry.get()
        if not os.path.exists(install_location):
            os.makedirs(install_location)
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class ServerPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text="Installation Server", font=("Segoe UI", 16))
        self.label.pack()
        emptyLine(self, 16)
        self.combobox = ttk.Combobox(self, values=list(SERVERS.keys()), width=50)
        self.combobox.pack()
        self.combobox.set(DEFAULT_SERVER)
        self.button = ttk.Button(self, text="Next", command=self.next, width=30)
        self.button.pack(pady=10)
    def next(self):
        global server
        global CURRENT_PAGE
        server = SERVERS[self.combobox.get()]
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class BranchPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text="Branch", font=("Segoe UI", 16))
        self.label.pack()
        emptyLine(self, 16)
        self.combobox = ttk.Combobox(self, values=list(BRANCHES.keys()), width=50)
        self.combobox.pack()
        self.combobox.set("main")
        self.button = ttk.Button(self, text="Next", command=self.next, width=30)
        self.button.pack(pady=10)
    def next(self):
        global branch
        global CURRENT_PAGE
        branch = BRANCHES[self.combobox.get()]
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class DisclaimerPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text=f"This program will:\n- Clone the repository ({install_location})\n- Create a Python virtual environment\n- Install the requirements\n- Create a run.bat file\n- Create a shortcut on the desktop and start menu\n\nThe program will not run the application")
        self.label.pack()
        self.button = ttk.Button(self, text="Next", command=self.next, width=30)
        self.button.pack(pady=10)
    def next(self):
        global CURRENT_PAGE
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class ClonePage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.pack_propagate(False)
        emptyLine(self, 40)
        self.label = ttk.Label(self, text="Clone repository", font=("Segoe UI", 16))
        self.label.pack()
        self.button = ttk.Button(self, text="Clone", command=self.clone, width=30)
        self.button.pack(pady=10)
    def clone(self):
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=WINDOW_WIDTH//2, maximum=40)
        self.progress.pack()
        import subprocess
        global install_location
        global server
        global branch
        self.progress.start(interval=20)
        self.button.config(text="Cloning", state="disabled")
        os.chdir(install_location)
        def cloneThread():
            subprocess.run(["git", "clone", "--branch", branch, server, "app"])
            self.progress.stop()
            self.progress.pack_forget()
            self.label.config(text="Repository cloned", foreground=PASTEL_GREEN)
            self.button.config(text="Next", command=self.next, state="normal")
        
        import threading
        thread = threading.Thread(target=cloneThread)
        thread.start()
        
        while thread.is_alive():
            self.master.update()
            self.update()
            time.sleep(0.02)
        

    def next(self):
        global CURRENT_PAGE
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class PythonVenvCreationPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text="Python virtual environment", font=("Segoe UI", 16))
        self.label.pack()
        self.button = ttk.Button(self, text="Create Venv", command=self.createVenv, width=30)
        self.button.pack(pady=10)

    def createVenv(self):
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=WINDOW_WIDTH//2, maximum=40)
        self.progress.pack()
        global install_location
        self.progress.start(interval=20)
        self.button.config(text="Creating Venv", state="disabled")
        self.master.update()
        def venvThread():
            os.chdir(install_location)
            # Run the command to create the virtual environment, run it in a way that microsoft defender doesn't block it
            os.system(f"cmd /c python -m venv venv")
            self.progress.stop()
            self.progress.pack_forget()
            self.label.config(text="Python virtual environment created", foreground=PASTEL_GREEN)
            self.button.config(text="Next", command=self.next, state="normal")
            
        import threading
        thread = threading.Thread(target=venvThread)
        thread.start()
        
        while thread.is_alive():
            self.master.update()
            self.update()
            time.sleep(0.02)
        
    def next(self):
        global CURRENT_PAGE
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class InstallRequirements(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.pack_propagate(False)
        emptyLine(self, 40)
        self.label = ttk.Label(self, text="Requirements installation", font=("Segoe UI", 16))
        self.label.pack()
        self.button = ttk.Button(self, text="Install", command=self.install, width=30)
        self.button.pack(pady=10)
    def install(self):
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=WINDOW_WIDTH//2, maximum=40)
        self.progress.pack()
        import subprocess
        global install_location
        self.progress.start(interval=20)
        self.button.config(text="Installing", state="disabled")
        self.master.update()
        os.chdir(install_location + "/app")
        def installThread():
            subprocess.run(["../venv/Scripts/python", "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.run(["../venv/Scripts/python", "-m", "pip", "install", "wheel"])
            subprocess.run(["../venv/Scripts/python", "-m", "pip", "install", "-r", "requirements.txt"])
            self.progress.stop()
            self.progress.pack_forget()
            self.label.config(text="Requirements installed", foreground=PASTEL_GREEN)
            self.button.config(text="Next", command=self.next, state="normal")

        import threading
        thread = threading.Thread(target=installThread)
        thread.start()
        
        while thread.is_alive():
            self.master.update()
            self.update()
            time.sleep(0.02)

    def next(self):
        global CURRENT_PAGE
        CURRENT_PAGE += 1
        self.pack_forget()
        next_page()

class RunPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text="Lane Assist installed", font=("Segoe UI", 16))
        self.label.pack()
        self.button = ttk.Button(self, text="Open Folder", command=self.run, width=30)
        self.button.pack(pady=10)
    def run(self):
        # Create the run.bat file
        fileContent = f'cmd /k "cd {install_location}/app & {install_location}/venv/Scripts/python main.py" & pause'
        with open(install_location + "/run.bat", "w") as file:
            file.write(fileContent)
        # Create the activate.bat file
        fileContent = f'cmd /k "cd {install_location}/venv/Scripts & .\\activate & cd {install_location}/app" & pause'
        with open(install_location + "/activate.bat", "w") as file:
            file.write(fileContent)
        # Open the folder, running would trigger antivirus
        os.startfile(install_location)
        sys.exit()

#endregion
#region Main logic
CURRENT_PAGE = 0
PAGE_ORDER = [
    CheckGitPage,
    CheckPythonPage,
    LocationPage, 
    ServerPage,
    BranchPage,
    DisclaimerPage,
    ClonePage,
    PythonVenvCreationPage,
    InstallRequirements,
    RunPage
]

totalPages = len(PAGE_ORDER) + 1
# Make a progress bar
progress = ttk.Progressbar(root, maximum=totalPages, length=WINDOW_WIDTH, value=0)
progress.pack()

def next_page():
    global CURRENT_PAGE
    if CURRENT_PAGE < len(PAGE_ORDER):
        PAGE_ORDER[CURRENT_PAGE](root).pack(anchor="center", side="top", expand=True)
    progress.step()

next_page()
#endregion
#region Tkinter theming
sv.set_theme("dark")

# Color the title bar
root.update()
colorTitleBar()
#endregion

root.mainloop()