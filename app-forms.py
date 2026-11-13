import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


# --- BANCO DE DADOS ---
def conectar_banco():
    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT
        )
    """)
    conexao.commit()
    conexao.close()


# --- FUNÇÃO PARA SALVAR CLIENTE ---
def salvar_cliente():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    telefone = entry_telefone.get().strip()

    if not nome or not email:
        messagebox.showwarning("Aviso", "Os campos Nome e E-mail são obrigatórios!")
        return

    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
        (nome, email, telefone),
    )
    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)


# --- NOVA FUNCIONALIDADE: VISUALIZAR CLIENTES ---
def visualizar_clientes():
    # Cria uma nova janela secundária
    janela_lista = tk.Toplevel(janela)
    janela_lista.title("Clientes Cadastrados")
    janela_lista.geometry("500x350")

    # Configura a tabela (Treeview) para exibir os dados
    colunas = ("ID", "Nome", "E-mail", "Telefone")
    tabela = ttk.Treeview(janela_lista, columns=colunas, show="headings")

    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")
    tabela.heading("E-mail", text="E-mail")
    tabela.heading("Telefone", text="Telefone")

    tabela.column("ID", width=40, anchor="center")
    tabela.column("Nome", width=160)
    tabela.column("E-mail", width=180)
    tabela.column("Telefone", width=100, anchor="center")

    tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Busca todos os clientes no banco de dados
    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email, telefone FROM clientes")
    registros = cursor.fetchall()
    conexao.close()

    # Insere cada cliente na tabela
    for cliente in registros:
        tabela.insert("", tk.END, values=cliente)


# --- INTERFACE PRINCIPAL ---
conectar_banco()

janela = tk.Tk()
janela.title("Cadastro de Clientes")
janela.geometry("350x280")

# Campos do formulário
tk.Label(janela, text="Nome:").pack(pady=(15, 2))
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack()

tk.Label(janela, text="E-mail:").pack(pady=(10, 2))
entry_email = tk.Entry(janela, width=40)
entry_email.pack()

tk.Label(janela, text="Telefone:").pack(pady=(10, 2))
entry_telefone = tk.Entry(janela, width=40)
entry_telefone.pack()

# Botões de ação
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

btn_salvar = tk.Button(
    frame_botoes,
    text="Cadastrar Cliente",
    command=salvar_cliente,
    bg="#4CAF50",
    fg="white",
    width=16,
)
btn_salvar.pack(side=tk.LEFT, padx=5)

# Novo botão solicitado
btn_visualizar = tk.Button(
    frame_botoes,
    text="Visualizar Clientes",
    command=visualizar_clientes,
    bg="#2196F3",
    fg="white",
    width=16,
)
btn_visualizar.pack(side=tk.LEFT, padx=5)

janela.mainloop()
