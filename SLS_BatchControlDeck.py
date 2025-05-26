# SLS_BatchControlDeck.py
# Stable LoRA Studio - Batch Execution Manager v1.2

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests
import time

# Load config
CONFIG_PATH = os.path.join("config", "sls_config.json")
PROMPT_PATH = os.path.join("config", "prompt_manifest.json")

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError("Missing sls_config.json. Run SLS_SetupWizard.py first.")

with open(CONFIG_PATH) as f:
    config = json.load(f)

API_URL = config["api_url"]

# Load saved prompts
def load_prompts():
    if not os.path.exists(PROMPT_PATH):
        return []
    with open(PROMPT_PATH) as f:
        return json.load(f)

# Execute prompt via API
def send_prompt(prompt, batch_size, cooldown):
    payload = {
        "prompt": f"{prompt['positive_prompt']} {prompt.get('lora_prompt', '')}",
        "negative_prompt": prompt.get("negative_prompt", ""),
        "sampler_name": prompt.get("sampler", "Euler a"),
        "steps": int(prompt.get("steps", 30)),
        "cfg_scale": float(prompt.get("cfg_scale", 5.5)),
        "width": int(prompt.get("width", 512)),
        "height": int(prompt.get("height", 768)),
        "n_iter": batch_size,
        "override_settings": {
            "sd_model_checkpoint": prompt["model"]
        },
        "save_images": True
    }

    response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
    if response.status_code == 200:
        print(f"✓ Success: {prompt['title'] or prompt['positive_prompt'][:30]}...")
    else:
        print(f"✗ Failure: {response.status_code} - {response.text}")
    time.sleep(cooldown)

# UI Logic
def run_selected():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("No Selection", "Select at least one prompt.")
        return
    try:
        batch_size = int(batch_size_entry.get())
        cooldown = int(cooldown_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Batch size and cooldown must be integers.")
        return

    for i in selected:
        send_prompt(prompts[i], batch_size, cooldown)

# UI Setup
prompts = load_prompts()

root = tk.Tk()
root.title("Stable LoRA Studio - Batch Control Deck")
root.geometry("700x500")

# Settings
tk.Label(root, text="Batch Size (images per prompt):").pack(pady=(10, 0))
batch_size_entry = tk.Entry(root)
batch_size_entry.insert(0, "5")
batch_size_entry.pack()

tk.Label(root, text="Cooldown Between Prompts (seconds):").pack(pady=(10, 0))
cooldown_entry = tk.Entry(root)
cooldown_entry.insert(0, "60")
cooldown_entry.pack()

# Prompt List
tk.Label(root, text="Select Prompts to Generate:").pack(pady=(10, 0))
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100)
listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

for idx, p in enumerate(prompts):
    label = f"{idx+1}. [{p['model']}] {p['title'] if 'title' in p else p['positive_prompt'][:40]}"
    listbox.insert(tk.END, label)

# Execute Button
tk.Button(root, text="Execute Selected Batches", command=run_selected).pack(pady=20)

root.mainloop()
