import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

PYTHON_CMD = "python3" if sys.platform != "win32" else "python" # python3 = linux; python = windows

SCRIPTS_DIR = "scripts" # Pasta onde estão os scripts

def listar_scripts():
    """Lista todos os arquivos Python na pasta de scripts."""
    return [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py")]

def executar_script(script):
    """Executa o script selecionado."""
    caminho = os.path.join(SCRIPTS_DIR, script)
    try:
        subprocess.run([PYTHON_CMD, caminho], check=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível executar {script}\n\n{e}")

# Criando a interface
root = tk.Tk()
root.title("Executar Scripts")
root.geometry("600x400")

scripts = listar_scripts()

# Criando os botões dinamicamente
for script in scripts:
    btn = tk.Button(root, text=script, command=lambda s=script: executar_script(s))
    btn.pack(pady=5)

# Rodando a interface
root.mainloop()