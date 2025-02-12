import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

def json_para_csv(json_file, csv_file):
    try:
        # Abrindo o arquivo JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Identificar todos os campos possíveis (pois alguns podem estar ausentes em certos registros)
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())  # Coletamos todas as chaves únicas

        # Abrindo o arquivo CSV para escrita
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))  # Garantir ordem fixa
            writer.writeheader()  # Escreve cabeçalhos
            for item in data:
                writer.writerow({key: item.get(key, "N/A") for key in all_keys})

        messagebox.showinfo("Sucesso", f"Conversão concluída! Arquivo salvo como {csv_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def csv_para_json(csv_file, json_file):
    try:
        # Abrindo o arquivo CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]

        # Salvando como JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Sucesso", f"Conversão concluída! Arquivo salvo como {json_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_arquivo(converter_funcao, extensao_origem, extensao_destino):
    arquivo_origem = filedialog.askopenfilename(filetypes=[(f"Arquivos {extensao_origem}", f"*.{extensao_origem}")])
    if arquivo_origem:
        arquivo_destino = arquivo_origem.rsplit('.', 1)[0] + f'.{extensao_destino}'
        converter_funcao(arquivo_origem, arquivo_destino)

# Criando a interface gráfica
root = tk.Tk()
root.title("Conversor JSON/CSV")
root.geometry("400x250")

tk.Label(root, text="Selecione o tipo de conversão:", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Converter JSON → CSV", command=lambda: selecionar_arquivo(json_para_csv, "json", "csv"), width=30).pack(pady=5)
tk.Button(root, text="Converter CSV → JSON", command=lambda: selecionar_arquivo(csv_para_json, "csv", "json"), width=30).pack(pady=5)

tk.Button(root, text="Sair", command=root.quit, width=15, bg="red", fg="white").pack(pady=20)

root.mainloop()
