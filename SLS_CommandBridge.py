# SLS_CommandBridge.py
# Stable LoRA Studio - Command Bridge v1.3 (Responsive Execution Edition)

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading
import time

# Define paths to module scripts
SCRIPTS = {
    "Setup Wizard": "SLS_SetupWizard.py",
    "Prompt Workbench": "SLS_PromptWorkbench.py",
    "Batch Control Deck": "SLS_BatchControlDeck.py"
}

PROGRESS_LOG = os.path.join("config", "batch_progress.txt")
STOP_FILE = os.path.join("config", "abort_signal.txt")

# Launch script handler (non-blocking, responsive)
def launch_script(script_name):
    path = SCRIPTS[script_name]
    if not os.path.exists(path):
        messagebox.showerror("Missing File", f"{path} not found.")
        return
    threading.Thread(target=lambda: subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)).start()

# Abort mission signal
def abort_mission():
    with open(STOP_FILE, "w") as f:
        f.write("ABORT")
    messagebox.showinfo("Abort Signal Sent", "Abort signal dispatched to batch runner.")

# Monitor progress
def update_progress():
    progress_box.delete(1.0, tk.END)
    if os.path.exists(PROGRESS_LOG):
        with open(PROGRESS_LOG) as f:
            lines = f.readlines()
            for line in lines[-20:]:  # Show last 20 lines
                progress_box.insert(tk.END, line)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(PROGRESS_LOG)))
        last_updated_var.set(f"Last Updated: {timestamp}")
    else:
        last_updated_var.set("No progress log detected.")
    root.after(5000, update_progress)

# Main GUI
root = tk.Tk()
root.title("Stable LoRA Studio - Command Bridge")
root.geometry("700x520")
root.configure(padx=20, pady=20)

# Header
tk.Label(root, text="Stable LoRA Studio", font=("Segoe UI", 16, "bold")).pack()
tk.Label(root, text="Command Bridge Dashboard", font=("Segoe UI", 12)).pack(pady=(0, 15))

# Launch Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
for label in SCRIPTS.keys():
    tk.Button(button_frame, text=label, width=25, height=2, command=lambda l=label: launch_script(l)).pack(pady=4)

# Abort Button
tk.Button(root, text="Abort Mission", bg="red", fg="white", width=25, command=abort_mission).pack(pady=(5, 15))

# Progress Monitor
tk.Label(root, text="Progress Log:").pack()
progress_box = tk.Text(root, height=12, width=80)
progress_box.pack()

# Last Updated Timestamp
last_updated_var = tk.StringVar()
tk.Label(root, textvariable=last_updated_var, font=("Segoe UI", 9)).pack(pady=(5, 0))

# Kick off log monitor loop
update_progress()

root.mainloop()
