import json
from tkinter import Tk, filedialog, messagebox, simpledialog

def remover_campos(json_data, campos_para_remover):
    """
    Remove os campos especificados de um dicionário ou lista de dicionários.
    """
    if isinstance(json_data, dict):
        # Remove os campos do dicionário
        for campo in campos_para_remover:
            json_data.pop(campo, None)  # Usamos pop com None para evitar erros se o campo não existir
        # Aplica a função recursivamente aos valores restantes
        for chave, valor in json_data.items():
            json_data[chave] = remover_campos(valor, campos_para_remover)
    elif isinstance(json_data, list):
        # Aplica a função recursivamente a cada item da lista
        json_data = [remover_campos(item, campos_para_remover) for item in json_data]
    return json_data

def salvar_json(dados, caminho_saida):
    """
    Salva os dados em um arquivo JSON.
    """
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

def main():
    # Cria a janela principal
    root = Tk()
    root.title("Removedor de Campos JSON")
    root.geometry("600x400")
    # root.withdraw()  # Esconde a janela principal

    # Abre a caixa de diálogo para selecionar o arquivo JSON
    caminho_json = filedialog.askopenfilename(
        title="Selecione o arquivo JSON",
        filetypes=[("Arquivos JSON", "*.json")]
    )

    if not caminho_json:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado!")
        return

    # Pergunta ao usuário quais campos devem ser removidos
    campos_para_remover = simpledialog.askstring(
        "Campos para Remover",
        "Digite os campos que deseja remover (separados por vírgula):"
    )

    if not campos_para_remover:
        messagebox.showerror("Erro", "Nenhum campo especificado!")
        return

    # Converte a string de campos para uma lista, removendo espaços e campos vazios
    campos_para_remover = [campo.strip() for campo in campos_para_remover.split(",") if campo.strip()]

    try:
        # Carrega o arquivo JSON
        with open(caminho_json, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        # Remove os campos especificados
        dados_tratados = remover_campos(dados, campos_para_remover)

        # Pede ao usuário para escolher onde salvar o novo arquivo JSON
        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )

        if not caminho_saida:
            messagebox.showerror("Erro", "Nenhum local de salvamento especificado!")
            return

        # Salva o novo arquivo JSON
        salvar_json(dados_tratados, caminho_saida)

        messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_saida}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

if __name__ == "__main__":
    main()