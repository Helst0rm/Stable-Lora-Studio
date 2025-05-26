# SLS_SetupWizard.py
# Stable LoRA Studio - First Time Setup Wizard (corrected: scan LoRAs via API)

import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Paths
CONFIG_DIR = "config"
CONFIG_PATH = os.path.join(CONFIG_DIR, "sls_config.json")

# Default API endpoint
DEFAULT_API_URL = "http://localhost:7860"

# Setup window
class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Stable LoRA Studio - Setup Wizard")

        tk.Label(root, text="Enter your Stable Diffusion API URL:").pack(pady=(10, 0))
        self.api_entry = tk.Entry(root, width=50)
        self.api_entry.insert(0, DEFAULT_API_URL)
        self.api_entry.pack(pady=5)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

        self.test_button = tk.Button(root, text="Test Connection Only", command=self.test_connection)
        self.test_button.pack(pady=5)

        self.scan_button = tk.Button(root, text="Update Checkpoints & LoRAs", command=self.full_scan)
        self.scan_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Config & Finish", command=self.save_config, state=tk.DISABLED)
        self.save_button.pack(pady=(10, 15))

        self.detected_checkpoints = []
        self.detected_loras = []

    def test_connection(self):
        url = self.api_entry.get().strip()
        self.status_label.config(text="Testing API connection...", fg="blue")
        try:
            response = requests.get(f"{url}/sdapi/v1/sd-models", timeout=5)
            if response.status_code == 200:
                self.status_label.config(text=f"✓ Connection confirmed to {url}.", fg="green")
                self.save_button.config(state=tk.NORMAL)
            else:
                self.status_label.config(text=f"✗ Failed: {response.status_code}", fg="red")
        except Exception:
            self.status_label.config(text=f"✗ Connection Error", fg="red")

    def full_scan(self):
        url = self.api_entry.get().strip()
        self.status_label.config(text="Scanning checkpoints and LoRAs...", fg="blue")

        # Scan checkpoints via API
        try:
            response = requests.get(f"{url}/sdapi/v1/sd-models", timeout=5)
            if response.status_code == 200:
                self.detected_checkpoints = [m['model_name'] for m in response.json()]
            else:
                self.status_label.config(text=f"✗ Checkpoint scan failed: {response.status_code}", fg="red")
                return
        except Exception:
            self.status_label.config(text=f"✗ Checkpoint scan error.", fg="red")
            return

        # Scan LoRAs via API
        try:
            response = requests.get(f"{url}/sdapi/v1/loras", timeout=5)
            if response.status_code == 200:
                self.detected_loras = [lora['name'] for lora in response.json()]
            else:
                self.status_label.config(text=f"✗ LoRA scan failed: {response.status_code}", fg="red")
                return
        except Exception:
            self.status_label.config(text=f"✗ LoRA scan error.", fg="red")
            return

        self.status_label.config(text=f"✓ Scan complete. {len(self.detected_checkpoints)} checkpoints, {len(self.detected_loras)} LoRAs detected.", fg="green")
        self.save_button.config(state=tk.NORMAL)

    def save_config(self):
        url = self.api_entry.get().strip()
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({
                "api_url": url,
                "checkpoints": self.detected_checkpoints if self.detected_checkpoints else [],
                "loras": self.detected_loras if self.detected_loras else []
            }, f, indent=4)
        messagebox.showinfo("Stable LoRA Studio", "Configuration saved successfully.")
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()
