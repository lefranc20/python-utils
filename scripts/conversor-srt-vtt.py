import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import subprocess
import sys

# Tenta importar chardet, instala automaticamente se não estiver presente
try:
    import chardet
except ModuleNotFoundError:
    messagebox.showinfo("Instalação", "A biblioteca 'chardet' não foi encontrada. Instalando automaticamente...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "chardet"])
    import chardet  # Tenta importar novamente após a instalação

def detectar_codificacao(arquivo):
    """Detecta a codificação de um arquivo."""
    with open(arquivo, 'rb') as f:
        resultado = chardet.detect(f.read())
        return resultado['encoding']

def ler_arquivo(arquivo):
    """Lê um arquivo com a codificação detectada automaticamente."""
    encoding_detectado = detectar_codificacao(arquivo)
    with open(arquivo, 'r', encoding=encoding_detectado, errors='replace') as file:
        return file.readlines(), encoding_detectado

def escrever_arquivo(arquivo, conteudo, encoding_destino="utf-8"):
    """Escreve um arquivo com a codificação especificada."""
    with open(arquivo, 'w', encoding=encoding_destino) as file:
        file.writelines(conteudo)

def converter_srt_para_vtt(arquivo_srt, arquivo_vtt):
    """Converte um arquivo .srt para .vtt"""
    try:
        srt_conteudo, encoding_origem = ler_arquivo(arquivo_srt)
        vtt_conteudo = ['WEBVTT\n\n']

        for linha in srt_conteudo:
            if re.match(r'^\d+$', linha.strip()):
                continue
            linha = linha.replace(',', '.')
            vtt_conteudo.append(linha)

        escrever_arquivo(arquivo_vtt, vtt_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def converter_vtt_para_srt(arquivo_vtt, arquivo_srt):
    """Converte um arquivo .vtt para .srt"""
    try:
        vtt_conteudo, encoding_origem = ler_arquivo(arquivo_vtt)
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

        escrever_arquivo(arquivo_srt, srt_conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_arquivo(converter_funcao, extensao_origem, extensao_destino):
    """Permite ao usuário selecionar um arquivo para conversão."""
    arquivo_origem = filedialog.askopenfilename(filetypes=[(f"Arquivos {extensao_origem}", f"*.{extensao_origem}")])
    if arquivo_origem:
        arquivo_destino = arquivo_origem.rsplit('.', 1)[0] + f'.{extensao_destino}'
        converter_funcao(arquivo_origem, arquivo_destino)
        messagebox.showinfo("Sucesso", f"Conversão concluída! Arquivo salvo como {arquivo_destino}")

def converter_pasta_srt_para_vtt():
    """Permite ao usuário selecionar uma pasta e converte todos os arquivos .srt para .vtt."""
    pasta_origem = filedialog.askdirectory()
    if not pasta_origem:
        return  # Usuário cancelou a seleção

    arquivos_srt = [f for f in os.listdir(pasta_origem) if f.endswith(".srt")]

    if not arquivos_srt:
        messagebox.showinfo("Aviso", "Nenhum arquivo .srt encontrado na pasta selecionada.")
        return

    for arquivo in arquivos_srt:
        caminho_srt = os.path.join(pasta_origem, arquivo)
        caminho_vtt = os.path.join(pasta_origem, arquivo.rsplit('.', 1)[0] + ".vtt")
        converter_srt_para_vtt(caminho_srt, caminho_vtt)

    messagebox.showinfo("Sucesso", f"Conversão concluída! {len(arquivos_srt)} arquivos convertidos.")

# Criando a interface gráfica
root = tk.Tk()
root.title("Conversor de Legendas SRT/VTT")
root.geometry("600x400")

tk.Label(root, text="Selecione o tipo de conversão:", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Converter SRT → VTT", command=lambda: selecionar_arquivo(converter_srt_para_vtt, "srt", "vtt"), width=30).pack(pady=5)
tk.Button(root, text="Converter VTT → SRT", command=lambda: selecionar_arquivo(converter_vtt_para_srt, "vtt", "srt"), width=30).pack(pady=5)
tk.Button(root, text="Converter Pasta (SRT → VTT)", command=converter_pasta_srt_para_vtt, width=30, bg="blue", fg="white").pack(pady=5)

tk.Button(root, text="Sair", command=root.quit, width=15, bg="red", fg="white").pack(pady=20)

root.mainloop()