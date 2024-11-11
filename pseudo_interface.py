import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import biblioteca_camada_logica
import DAO
import datetime

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("400x500")
        
        # Cria o menu principal
        self.create_main_menu()
    
    def create_main_menu(self):
        self.clear_window()
        
        tk.Label(self.root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)
        buttons = [
            ("Cadastrar Bibliotecário", self.cadastrar_bibliotecario),
            ("Cadastrar Assistente", self.cadastrar_assistente),
            ("Cadastrar Usuário", self.cadastrar_usuario),
            ("Cadastrar Livro", self.cadastrar_livro),
            ("Cadastrar Exemplar", self.cadastrar_exemplar),
            ("Realizar Empréstimo", self.realizar_emprestimo),
            ("Localizar Exemplar", self.localizar_exemplar),
            ("Devolução de Exemplar", self.devolucao_exemplar),
            ("Renovar Empréstimo", self.renovar_emprestimo),
            ("Comandos do Desenvolvedor", self.menu_do_desenvolvedor),
            ("Sair", self.root.destroy)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=30).pack(pady=5)
    
    def cadastrar_bibliotecario(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Bibliotecário", font=("Arial", 16)).pack(pady=10)
        
        fields = ["CPF", "Nome", "Rua", "Cidade", "CEP", "Telefone", "Endereço"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        def submit():
            bibliotechman = biblioteca_camada_logica.Bibliotecario(
                entries["CPF"].get(), entries["Nome"].get(), entries["Rua"].get(), 
                entries["Cidade"].get(), entries["CEP"].get(), entries["Telefone"].get(), entries["Endereço"].get()
            )
            DAO.cadastrar_bibliotecario(bibliotechman)
            messagebox.showinfo("Sucesso", "Bibliotecário cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    def cadastrar_assistente(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Assistente", font=("Arial", 16)).pack(pady=10)
        
        fields = ["CPF", "Nome", "Rua", "Cidade", "CEP", "Telefone", "Endereço", "Supervisores (CPF separados por vírgula)"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        def submit():
            supervisores = entries["Supervisores (CPF separados por vírgula)"].get().split(",")
            assistente = biblioteca_camada_logica.Assistente(
                entries["CPF"].get(), entries["Nome"].get(), entries["Rua"].get(),
                entries["Cidade"].get(), entries["CEP"].get(), entries["Telefone"].get(), entries["Endereço"].get(), supervisores
            )
            DAO.cadastrar_assistente(assistente)
            messagebox.showinfo("Sucesso", "Assistente cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)

    def cadastrar_usuario(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Usuário", font=("Arial", 16)).pack(pady=10)
        
        fields = ["CPF", "Nome", "Rua", "Cidade", "CEP", "Telefone", "Endereço"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        tk.Label(self.root, text="Categoria").pack()
        categoria_var = tk.IntVar()
        categorias = [
            ("Aluno de graduação", 1),
            ("Aluno de pós-graduação", 2),
            ("Professor", 3),
            ("Professor de pós-graduação", 4)
        ]
        
        for text, value in categorias:
            tk.Radiobutton(self.root, text=text, variable=categoria_var, value=value).pack(anchor="w")
        
        def submit():
            categoria_map = {
                1: {'id': 1, 'Categoria': 'Aluno de graduação'},
                2: {'id': 2, 'Categoria': "Aluno de pós-graduação"},
                3: {'id': 3, 'categoria': 'Professor'},
                4: {'id': 4, 'categoria': "Professor de pós-graduação"}
            }
            
            usuario = biblioteca_camada_logica.Usuario(
                entries["CPF"].get(), entries["Nome"].get(), entries["Rua"].get(), 
                entries["Cidade"].get(), entries["CEP"].get(), entries["Telefone"].get(), 
                entries["Endereço"].get(), 0, categoria_map[categoria_var.get()]
            )
            DAO.cadastrar_usuario(usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    def cadastrar_livro(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Livro", font=("Arial", 16)).pack(pady=10)
        
        fields = ["Título", "Autores (separados por vírgula)", "ISBN", "Editora", "Coleção"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        def submit():
            autores = entries["Autores (separados por vírgula)"].get().split(",")
            livro = biblioteca_camada_logica.Livro(
                entries["Título"].get(), autores, entries["ISBN"].get(), 
                entries["Editora"].get(), entries["Coleção"].get()
            )
            DAO.cadastrar_livro(livro)
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    def cadastrar_exemplar(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Exemplar", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.root, text="ISBN").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        num_entry = tk.Entry(self.root)
        num_entry.pack()
        
        tk.Label(self.root, text="Status").pack()
        status_var = tk.StringVar(value="Disponível")
        tk.Radiobutton(self.root, text="Disponível", variable=status_var, value="Disponível").pack(anchor="w")
        tk.Radiobutton(self.root, text="Indisponível", variable=status_var, value="Indisponível").pack(anchor="w")
    
        
        def submit():
            if not DAO.verificar_isbn(isbn_entry.get()):
                messagebox.showwarning("Erro", "ISBN não encontrado no banco de dados!")
                return
            
            if DAO.get_exemplar(isbn_entry.get(), int(num_entry.get())):
                messagebox.showwarning("Erro", "Exemplar já cadastrado!")
                return
            
            exemplar = biblioteca_camada_logica.Exemplar(int(num_entry.get()), status_var.get())
            DAO.cadastrar_exemplar(exemplar, isbn_entry.get())
            messagebox.showinfo("Sucesso", "Exemplar cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    
    
    def realizar_emprestimo(self):
        self.clear_window()
        tk.Label(self.root, text="Realizar Empréstimo", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para realizar o empréstimo
        tk.Label(self.root, text="ISBN").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        tk.Label(self.root, text="CPF do Usuário").pack()
        cpf_entry = tk.Entry(self.root)
        cpf_entry.pack()
        
        def submit():
            try:
                # Verificação dos dados do usuário e exemplar
                ISBN = isbn_entry.get()
                num_exemplar = int(exemplar_entry.get())
                CPF = cpf_entry.get()
                
                usuario = DAO.get_usuario(CPF)
                if not usuario:
                    messagebox.showwarning("Erro", "Usuário não encontrado!")
                    return
                
                # Define a quantidade de dias com base na categoria do usuário
                categoria = usuario['Categoria']['Categoria']
                qtd_dias = {
                    "Aluno de graduação": 15,
                    "Aluno de pós-graduação": 30,
                    "Professor": 30,
                    "Professor de pós-graduação": 90
                }.get(categoria, 15)
                
                data_hoje = datetime.date.today()
                emprestimo = biblioteca_camada_logica.Emprestimo(data_hoje, ISBN, num_exemplar, CPF, qtd_dias)
                biblioteca_camada_logica.emprestar_livro(emprestimo, data_hoje)
                
                messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira dados válidos.")
        
        tk.Button(self.root, text="Realizar Empréstimo", command=submit).pack(pady=20)
    
    
    
    
    def localizar_exemplar(self):
        self.clear_window()
        tk.Label(self.root, text="Localizar Exemplar", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para localizar o exemplar
        tk.Label(self.root, text="ISBN").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        def buscar_exemplar():
            try:
                ISBN = isbn_entry.get()
                numero = int(exemplar_entry.get())
                
                # Usa a função DAO.get_exemplar para localizar o exemplar
                exemplar = DAO.get_exemplar(ISBN, numero)
                if exemplar:
                    messagebox.showinfo("Exemplar Encontrado", f"Exemplar: {exemplar}")
                else:
                    messagebox.showwarning("Não Encontrado", "Exemplar não encontrado!")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um número válido para o exemplar.")
        
        tk.Button(self.root, text="Buscar Exemplar", command=buscar_exemplar).pack(pady=20)
        tk.Button(self.root, text="Voltar", command=self.create_main_menu).pack(pady=10)

    def devolucao_exemplar(self):
        self.clear_window()
        tk.Label(self.root, text="Devolução de Exemplar", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para devolução de exemplar
        tk.Label(self.root, text="ISBN").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        tk.Label(self.root, text="Data de Devolução (DD-MM-YYYY)").pack()
        data_devolucao_entry = tk.Entry(self.root)
        data_devolucao_entry.pack()
        
        def devolver():
            try:
                ISBN = isbn_entry.get()
                num_exemplar = int(exemplar_entry.get())
                data_devolucao_str = data_devolucao_entry.get()
                data_devolucao = datetime.datetime.strptime(data_devolucao_str, "%d-%m-%Y").date()
                
                # Função para processar a devolução
                biblioteca_camada_logica.devolver_livro(ISBN, num_exemplar, data_devolucao)
                messagebox.showinfo("Sucesso", "Devolução realizada com sucesso!")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira dados válidos.")
        
        tk.Button(self.root, text="Devolver Exemplar", command=devolver).pack(pady=20)
        tk.Button(self.root, text="Voltar", command=self.create_main_menu).pack(pady=10)

    
    

    def renovar_emprestimo(self):
        self.clear_window()
        tk.Label(self.root, text="Renovar Empréstimo", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para renovação de empréstimo
        tk.Label(self.root, text="ISBN").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        tk.Label(self.root, text="Data de Hoje (DD-MM-YYYY)").pack()
        data_hoje_entry = tk.Entry(self.root)
        data_hoje_entry.pack()
        
        def renovar():
            try:
                ISBN = isbn_entry.get()
                num_exemplar = int(exemplar_entry.get())
                data_hoje_str = data_hoje_entry.get()
                data_hoje = datetime.datetime.strptime(data_hoje_str, "%d-%m-%Y").date()
                
                # Função para processar a renovação
                biblioteca_camada_logica.renovar_emprestimo(ISBN, num_exemplar, data_hoje)
                messagebox.showinfo("Sucesso", "Renovação realizada com sucesso!")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira dados válidos.")
        
        tk.Button(self.root, text="Renovar Empréstimo", command=renovar).pack(pady=20)
        tk.Button(self.root, text="Voltar", command=self.create_main_menu).pack(pady=10)

    def menu_do_desenvolvedor(self):
        self.clear_window()
        tk.Label(self.root, text="Comandos do Desenvolvedor", font=("Arial", 16)).pack(pady=10)
        
        buttons = [
            ("Visualizar Bibliotecários", self.visualizar_bibliotecarios),
            ("Visualizar Assistentes", self.visualizar_assistentes),
            ("Visualizar Usuários", self.visualizar_usuarios),
            ("Visualizar Livros", self.visualizar_livros),
            ("Visualizar Exemplares", self.visualizar_exemplares),
            ("Visualizar Empréstimos", self.visualizar_emprestimos),
            ("Voltar", self.create_main_menu)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=30).pack(pady=5)

    def visualizar_bibliotecarios(self):
        self.display_data("Bibliotecários", DAO.get_bibliotecarios())
    
    def visualizar_assistentes(self):
        self.display_data("Assistentes", DAO.get_assistentes())
    
    def visualizar_usuarios(self):
        self.display_data("Usuários", DAO.get_usuarios())
    
    def visualizar_livros(self):
        self.display_data("Livros", DAO.get_livros())
    
    def visualizar_exemplares(self):
        ISBN = tk.simpledialog.askstring("ISBN", "Digite o ISBN:")
        exemplares = DAO.get_exemplares(ISBN)
        self.display_data("Exemplares", exemplares)
    
    def visualizar_emprestimos(self):
        self.display_data("Empréstimos", DAO.get_todos_emprestimos())

    def display_data(self, title, data):
        self.clear_window()
        
        tk.Label(self.root, text=title, font=("Arial", 16)).pack(pady=10)
        
        # Verifica se há dados a serem exibidos
        if not data:
            tk.Label(self.root, text="Nenhum dado disponível", font=("Arial", 12)).pack(pady=10)
            return
        
        # Cria o Treeview (tabela)
        columns = list(data[0].keys())  # Usa as chaves do primeiro item como nomes das colunas
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        # Define as colunas e os cabeçalhos
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        # Insere cada item na tabela
        for item in data:
            values = [item[col] for col in columns]  # Pega os valores na ordem das colunas
            tree.insert("", tk.END, values=values)
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Botão para voltar
        tk.Button(self.root, text="Voltar", command=self.menu_do_desenvolvedor).pack(pady=10)


    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Inicialização da interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
