# Stable LoRA Studio (SLS)

**Stable LoRA Studio** is a local GUI-based toolkit for building and running prompt datasets for LoRA training. Built in Python with Tkinter, it integrates with a Stable Diffusion instance via the WebUI API.

## Features
- 🔧 Setup Wizard for environment detection and config
- 🧠 Prompt Workbench for multi-LoRA prompt creation
- 🛰️ Batch Control Deck for automated dataset generation
- 🧭 Command Bridge dashboard to manage the whole suite

## Requirements
- Python 3.10+
- A running Stable Diffusion instance with the WebUI API (`http://localhost:7860`)
- API and Listen command args (--api --listen) for your version of Stable Diffusion (A1111, Forge, Reforge, etc)

## Installation
Clone the repo:
```bash
git clone https://github.com/helst0rm/stable-lora-studio.git
cd stable-lora-studio

Install Requirements:

pip install -r requirements.txt

Run the Command Bridge

python SLS_CommandBridge.py
