# SLS_PromptWorkbench.py
# Stable LoRA Studio - Prompt Workbench UI v1.5

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests

# Load config
CONFIG_PATH = os.path.join("config", "sls_config.json")
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError("Missing config file. Please run SLS_SetupWizard.py first.")

with open(CONFIG_PATH) as f:
    config = json.load(f)

API_URL = config["api_url"]
CHECKPOINTS = config.get("checkpoints", [])
LORAS = config.get("loras", [])

# Save prompt data
PROMPT_OUT = os.path.join("config", "prompt_manifest.json")

def format_lora_tags(lora_selections):
    formatted = []
    for lora_name, weight in lora_selections:
        if lora_name:
            weight_val = weight if weight else "1"
            formatted.append(f"<lora:{lora_name}:{weight_val}>")
    return " ".join(formatted)

def save_prompt():
    model = model_cb.get()
    title = title_entry.get().strip()
    pos_prompt = pos_entry.get("1.0", tk.END).strip()
    neg_prompt = neg_entry.get("1.0", tk.END).strip()
    notes = notes_entry.get("1.0", tk.END).strip()
    sampler = sampler_cb.get()
    steps = steps_entry.get().strip()
    cfg = cfg_entry.get().strip()
    width = width_entry.get().strip()
    height = height_entry.get().strip()

    lora_selections = [(lora_cb[i].get(), weight_entry[i].get()) for i in range(5)]
    lora_prompt = format_lora_tags(lora_selections)

    if not model or not pos_prompt or not title:
        messagebox.showerror("Missing Fields", "Model, title, and positive prompt are required.")
        return

    prompt = {
        "model": model,
        "title": title,
        "positive_prompt": pos_prompt,
        "negative_prompt": neg_prompt,
        "lora_prompt": lora_prompt,
        "notes": notes,
        "sampler": sampler,
        "steps": steps,
        "cfg_scale": cfg,
        "width": width,
        "height": height
    }

    os.makedirs("config", exist_ok=True)
    if os.path.exists(PROMPT_OUT):
        with open(PROMPT_OUT) as f:
            all_prompts = json.load(f)
    else:
        all_prompts = []

    all_prompts.append(prompt)
    with open(PROMPT_OUT, "w") as f:
        json.dump(all_prompts, f, indent=4)

    messagebox.showinfo("Saved", f"Prompt saved to {PROMPT_OUT}.")
    title_entry.delete(0, tk.END)
    pos_entry.delete("1.0", tk.END)
    neg_entry.delete("1.0", tk.END)
    notes_entry.delete("1.0", tk.END)
    for i in range(5):
        lora_cb[i].set("")
        weight_entry[i].delete(0, tk.END)
    sampler_cb.set("")
    steps_entry.delete(0, tk.END)
    cfg_entry.delete(0, tk.END)
    width_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

def clear_manifest():
    if os.path.exists(PROMPT_OUT):
        with open(PROMPT_OUT, "w") as f:
            json.dump([], f, indent=4)
        messagebox.showinfo("Cleared", "Prompt manifest has been cleared.")

# UI
root = tk.Tk()
root.title("Stable LoRA Studio - Prompt Workbench")
root.geometry("650x950")

# --- Model Selection ---
tk.Label(root, text="Select Checkpoint Model:").pack(pady=(10, 0))
model_cb = ttk.Combobox(root, width=60, values=CHECKPOINTS)
model_cb.pack(pady=5)

# --- Prompt Title ---
tk.Label(root, text="Prompt Title:").pack(pady=(10, 0))
title_entry = tk.Entry(root, width=70)
title_entry.pack(pady=5)

# --- Positive Prompt Input ---
tk.Label(root, text="Enter Positive Prompt:").pack(pady=(10, 0))
pos_entry = tk.Text(root, width=70, height=5)
pos_entry.pack(pady=5)

# --- Negative Prompt Input ---
tk.Label(root, text="Enter Negative Prompt (optional):").pack(pady=(10, 0))
neg_entry = tk.Text(root, width=70, height=3)
neg_entry.pack(pady=5)

# --- LoRA Inputs ---
tk.Label(root, text="Select up to 5 LoRAs and weights:").pack(pady=(10, 0))
lora_cb = []
weight_entry = []
for i in range(5):
    frame = tk.Frame(root)
    frame.pack(pady=2)
    cb = ttk.Combobox(frame, width=50, values=LORAS)
    cb.pack(side=tk.LEFT, padx=5)
    lora_cb.append(cb)
    w_entry = tk.Entry(frame, width=10)
    w_entry.pack(side=tk.LEFT)
    weight_entry.append(w_entry)

# --- Info Message ---
tk.Label(root, text="If no weight is entered, default of 1 will be applied.", fg="gray").pack(pady=(0, 10))

# --- Sampler/Steps/CFG/Resolution ---
tk.Label(root, text="Sampler:").pack()
sampler_cb = ttk.Combobox(root, width=60, values=["Euler a", "Euler", "DPM++ 2M Karras", "DDIM", "Heun", "DPM++ SDE Karras"])
sampler_cb.pack(pady=2)

frame_gen = tk.Frame(root)
frame_gen.pack(pady=2)
tk.Label(frame_gen, text="Steps:").pack(side=tk.LEFT)
steps_entry = tk.Entry(frame_gen, width=5)
steps_entry.pack(side=tk.LEFT, padx=(5, 10))
tk.Label(frame_gen, text="CFG Scale:").pack(side=tk.LEFT)
cfg_entry = tk.Entry(frame_gen, width=5)
cfg_entry.pack(side=tk.LEFT, padx=(5, 10))
tk.Label(frame_gen, text="Width:").pack(side=tk.LEFT)
width_entry = tk.Entry(frame_gen, width=6)
width_entry.pack(side=tk.LEFT, padx=(5, 10))
tk.Label(frame_gen, text="Height:").pack(side=tk.LEFT)
height_entry = tk.Entry(frame_gen, width=6)
height_entry.pack(side=tk.LEFT)

# --- Prompt Notes ---
tk.Label(root, text="Notes (optional):").pack(pady=(10, 0))
notes_entry = tk.Text(root, width=70, height=3)
notes_entry.pack(pady=5)

# --- Save Button ---
save_btn = tk.Button(root, text="Save Prompt to Manifest", command=save_prompt)
save_btn.pack(pady=10)

# --- Clear Manifest Button ---
clear_btn = tk.Button(root, text="Clear Prompt Manifest (Deletes all prompts)", command=clear_manifest, fg="red")
clear_btn.pack(pady=(5, 15))

root.mainloop()
