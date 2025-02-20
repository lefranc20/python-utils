import tkinter as tk
from tkinter import filedialog, messagebox
import re

def converter_srt_para_vtt(arquivo_srt, arquivo_vtt):
    """Converte um arquivo .srt para .vtt"""
    try:
        with open(arquivo_srt, 'r', encoding='utf-8') as file:
            srt_conteudo = file.readlines()
        
        vtt_conteudo = ['WEBVTT\n\n']
        
        for linha in srt_conteudo:
            if re.match(r'^\d+$', linha.strip()):
                continue
            linha = linha.replace(',', '.')
            vtt_conteudo.append(linha)
        
        with open(arquivo_vtt, 'w', encoding='utf-8') as file:
            file.writelines(vtt_conteudo)
        
        messagebox.showinfo("Sucesso", f"Conversão concluída! Arquivo salvo como {arquivo_vtt}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def converter_vtt_para_srt(arquivo_vtt, arquivo_srt):
    """Converte um arquivo .vtt para .srt"""
    try:
        with open(arquivo_vtt, 'r', encoding='utf-8') as file:
            vtt_conteudo = file.readlines()
        
        srt_conteudo = []
        contador = 1
        
        for linha in vtt_conteudo:
            if "WEBVTT" in linha or linha.strip() == "":
                continue
            
            linha = linha.replace('.', ',')
            if "-->" in linha:
                srt_conteudo.append(f"{contador}\n")
                contador += 1
            
            srt_conteudo.append(linha)
        
        with open(arquivo_srt, 'w', encoding='utf-8') as file:
            file.writelines(srt_conteudo)
        
        messagebox.showinfo("Sucesso", f"Conversão concluída! Arquivo salvo como {arquivo_srt}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_arquivo(converter_funcao, extensao_origem, extensao_destino):
    arquivo_origem = filedialog.askopenfilename(filetypes=[(f"Arquivos {extensao_origem}", f"*.{extensao_origem}")])
    if arquivo_origem:
        arquivo_destino = arquivo_origem.rsplit('.', 1)[0] + f'.{extensao_destino}'
        converter_funcao(arquivo_origem, arquivo_destino)

# Criando a interface gráfica
root = tk.Tk()
root.title("Conversor de Legendas SRT/VTT")
root.geometry("600x400")

tk.Label(root, text="Selecione o tipo de conversão:", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Converter SRT → VTT", command=lambda: selecionar_arquivo(converter_srt_para_vtt, "srt", "vtt"), width=30).pack(pady=5)
tk.Button(root, text="Converter VTT → SRT", command=lambda: selecionar_arquivo(converter_vtt_para_srt, "vtt", "srt"), width=30).pack(pady=5)

tk.Button(root, text="Sair", command=root.quit, width=15, bg="red", fg="white").pack(pady=20)

root.mainloop()
