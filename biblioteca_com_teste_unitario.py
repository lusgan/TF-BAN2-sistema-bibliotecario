import unittest
from datetime import datetime, timedelta
import datetime
import DAO

# Classes da Biblioteca
class Livro:
    def __init__(self, titulo, autores, ISBN, editora, colecao,):
        self.titulo = titulo
        self.autores = autores #lista de autores
        self.ISBN = ISBN
        self.editora = editora
        self.colecao = colecao
        self.exemplares = []
         
    
    def to_json(self):
        json = { 'Titulo' : self.titulo, 'autores' : self.autores, 'ISBN' : self.ISBN, 'Editora' : self.editora, 'Colecao' : self.colecao, 'Exemplares' : self.exemplares}
        return json
    
    
    def nome_dos_autores_string(self):
        nomes = ""
        
        if isinstance(self.autores,list):
            
            for autor in self.autores:
                nomes = nomes + f"{autor.nome},"
        
        else:
            nomes = self.autores.nome
            
        return nomes


class Exemplar:
    def __init__(self, num, status):
        self.num = num
        self.status = status
        self.posse = None
        
    
    def to_json(self):
        json = { 'num' : self.num, 'status' : self.status, 'posse' : self.posse}
        return json
        
        

class Bibliotecario:
    def __init__(self,cpf, nome, rua, cidade, cep, telefone, endereco):
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        
    def to_json(self):
        json = {'CPF': self.cpf, 'Nome' : self.nome, 'Rua' : self.rua, 'Cidade' : self.cidade, 'CEP' : self.cep, 'Telefone' : self.telefone, 'Endereco' : self.endereco}
        return json


class Assistente:
    
    def __init__(self, cpf, nome, rua, cidade, cep, telefone, endereco, supervisores):
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.supervisores = supervisores

    def to_json(self):
         json = {'CPF': self.cpf, 'Nome' : self.nome, 'Rua' : self.rua, 'Cidade' : self.cidade, 'CEP' : self.cep, 'Telefone' : self.telefone, 'Endereco' : self.endereco, 'Supervisores' : self.supervisores}
         return json


class Usuario:
    
    def __init__(self,cpf, nome, rua, cidade, cep, telefone, endereco, multa, categoria):
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.multa = multa
        self.categoria = categoria
        self.emprestimos = None
        
    
    def to_json(self):
         json = {'CPF': self.cpf, 'Nome' : self.nome, 'Rua' : self.rua, 'Cidade' : self.cidade, 'CEP' : self.cep, 'Telefone' : self.telefone, 'Endereco' : self.endereco, 'Multa' : self.multa, 'Categoria' : self.categoria, "Emprestimos" : self.emprestimos}
         return json
    



class Autor:
    
    def __init__(self, nome):
        self.nome = nome
    


class Emprestimo:
    def __init__(self, data_hoje, ISBN, num_exemplar, CPF, qtd_dias):
        self.id_emprestimo = DAO.get_id_ultimo_emprestimo() + 1;
        self.dataInicial = data_hoje.strftime('%d-%m-%Y')
        self.dataFinal = (data_hoje + timedelta(days=qtd_dias)).strftime('%d-%m-%Y')
        self.dia_que_foi_devolvido = None
        self.ISBN =ISBN
        self.num_exemplar = num_exemplar
        self.CPF = CPF
        self.multa = None

    def devolver(self, data):
        self.livro.emprestado = False
        self.dia_que_foi_devolvido = data
        if data > self.dataFinal:
            self.usuario.penalizar(data, self)
    
    def to_json(self):
        
        json = {'id': self.id_emprestimo, 'Inicio' : self.dataInicial, 'Fim' : self.dataFinal, 'Data de devolucao' : self.dia_que_foi_devolvido, 'ISBN' : self.ISBN, 'exemplar' : self.num_exemplar, 'CPF' : self.CPF, 'Multa' : self.multa}
        return json
 

def usuario_possui_atraso(CPF, data_hoje):
    
    usuario = DAO.get_usuario(CPF)    
    emprestimos = usuario['emprestimos']    
    
    for emprestimo in emprestimos:
        data_fim_iso = emprestimo['Fim']
        
        data_fim = datetime.datetime.strptime(data_fim_iso, "%d-%m-%Y").date()
        
        if data_hoje > data_fim : 
            return True
        
        return False

def emprestar_livro(emprestimo,data_hoje):
    
    #Colocar condicoes para emprestimo como : 
    #nao ter livros atrasados ----> OK
    #nao ter multas ----> OK
    #nao exceder o limite de livros pegos emprestado --->OK
    #nao pode emprestar da colecao reserva
    #so pode emprestar livros disponiveis  -----> OK
    
    exemplar = DAO.get_exemplar(emprestimo.ISBN, emprestimo.num_exemplar)
    usuario = DAO.get_usuario(emprestimo.CPF)
    
    limite_de_emprestimos = 4
    emprestimos = usuario['emprestimos']
    qtd_emprestimos = len(emprestimos)
    
    
    if exemplar['status'] == 'Indisponivel':
        print("Exemplar indisponivel.\n")
        
    
    elif usuario_possui_atraso(emprestimo.CPF, data_hoje):
        print("Usuario possui livro com atraso.\n")
        
    
    elif usuario['Multa'] > 0:
        print("Usuario possui multa pendente.\n")
        
    
    elif qtd_emprestimos + 1 > limite_de_emprestimos: 
        print("Usuario ja atingiu limite de emprestimos!\n")
        
    elif DAO.get_colecao(emprestimo.ISBN).lower() == "reserva":
        print("Esse livro faz parte da colecao reserva, logo não pode ser emprestado.")
    
    else:
    
        DAO.atualizar_exemplar(emprestimo.ISBN, emprestimo.num_exemplar, "Indisponivel", emprestimo.CPF)
        DAO.adicionar_emprestimo_usuario(emprestimo)
    



def devolver_livro(ISBN, num_exemplar,data_devolucao):
    #apagar o emprestimo da lista de emprestimos do usuario ---> OK
    #manter emprestimo na colecao emprestimos  ------> OK
    #alterar data de devolucao no emprestimo ---->OK
    #atualizar status e posse do exemplar ------> OK
    #se houver atraso, cobrar multa ---> Ok
    
    emprestimo = DAO.get_emprestimo(ISBN, num_exemplar)
    multa = None
    
    if data_devolucao > datetime.datetime.strptime(emprestimo['Fim'], "%d-%m-%Y").date():
        multa = 30
    
    
    DAO.atualizar_emprestimo(ISBN, num_exemplar, data_devolucao.strftime('%d-%m-%Y'), multa)  
    DAO.atualizar_exemplar(ISBN, num_exemplar, 'Disponivel', None)
    DAO.apagar_emprestimo_usuario(emprestimo['CPF'], emprestimo['id'], multa)
    



class Biblioteca:
    def __init__(self):
        self.catalogo = {}
        self.usuarios = []
        self.emprestimos = []

    def adicionar_livro(self, livro):
        if livro.ISBN not in self.catalogo:
            self.catalogo[livro.ISBN] = [livro]
        else:
            self.catalogo[livro.ISBN].append(livro)

    def listar_livros(self):
        print("-" * 50)
        print("Catálogo de Livros:")
        for isbn, livros in self.catalogo.items():
            for livro in livros:
                print(f"Título: {livro.titulo}  Autores: [{livro.nome_dos_autores_string()}]   Ano: {livro.ano}   ISBN: {livro.ISBN}")
        print(f"\nTotal de livros = {sum(len(livros) for livros in self.catalogo.values())}")
        print("-" * 50)
        
    
    def listar_exemplares(self, livro):
        print("-"*40)
        print(f"Exemplares do livro {livro.titulo}\n")
        for l in self.catalogo[livro.ISBN]:
            print(f"Título: {l.titulo} | id: {l.id} | ano: {l.ano} | emprestado = {l.esta_emprestado()}")
        
        print(f"total de exemplares = {len(self.catalogo[livro.ISBN])}")

    def cadastrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def emprestar_livro(self, livro, usuario, data_hoje):
        if usuario.possui_penalidade(data_hoje):
            print(f"Usuário {usuario.nome} está sob penalidade. Empréstimo não realizado.")
            return False

        
        elif livro.id==0:
            print("Esse livro nao pode ser emprestado pela biblioteca")
            return False
        

        else:  #os livros de id 0 nao devem ser emprestados
            emprestimo = Emprestimo(len(self.emprestimos), data_hoje, livro, usuario)
            self.emprestimos.append(emprestimo)
            livro.emprestado = True
            usuario.historico_de_emprestimos.append(emprestimo)
            print(f"Livro '{livro.titulo}' emprestado para {usuario.nome}. Devolução até {emprestimo.dataFinal}.")
            return True
        

    def devolver_livro(self, livro, data):
        for emprestimo in self.emprestimos:
            if emprestimo.livro == livro:
                emprestimo.devolver(data)
                print(f"Livro '{livro.titulo}' devolvido.")
                





'''
# Teste das funcionalidades
biblioteca = Biblioteca()
autor1 = Autor("Lucas o brabo")
autor2 = Autor("Gabriel")
# Instanciando 15 livros diferentes
livros = [
    Livro(0, "quimica organica", [autor1,autor2], 2024, 1),
    Livro(0, "quimica radical", autor1, 2022, 2),
    Livro(1, "quimica organica", autor2, 2024, 3),
    Livro(0, "fisica basica", autor1 , 2021, 4),
    Livro(0, "matematica pura", autor2 , 2020, 5),
    Livro(0, "biologia geral", autor1, 2019, 6),
    Livro(0, "historia do mundo", autor2, 2018, 7),
    Livro(0, "geografia fisica", autor1, 2017, 8),
    Livro(0, "programacao em Python", autor2, 2023, 9),
    Livro(0, "inteligencia artificial", autor1, 2023, 10),
    Livro(0, "algoritmos", autor2 , 2022, 11),
    Livro(0, "engenharia de software", autor1, 2021, 12),
    Livro(0, "redes de computadores", autor2 , 2020, 13),
    Livro(0, "sistemas operacionais", autor1 , 2019, 14),
    Livro(0, "banco de dados", autor2 , 2018, 15)
]

# Adicionando 3 exemplares de cada livro na biblioteca
for livro in livros:
    for id in range(3):
        copia = Livro(id, livro.titulo, livro.autores, livro.ano, livro.ISBN)
        biblioteca.adicionar_livro(copia)

# Listar todos os livros na biblioteca
biblioteca.listar_livros()

# Cadastrar um usuário
usuario1 = Usuario(101, "Lucas", "apapa@example.com")
biblioteca.cadastrar_usuario(usuario1)

# Escolher um livro para emprestar
livroEscolhido = biblioteca.catalogo[1][0]
biblioteca.emprestar_livro(livroEscolhido, usuario1, datetime(2024, 6, 18))

# Listar exemplares de um dos livros
biblioteca.listar_exemplares(livroEscolhido)
'''



# Testes unitários
class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        self.biblioteca = Biblioteca()
        
        
        #definicao de autores
        self.autor1 = Autor("eu e mais 2")
        self.autor2 = Autor("Autor x")
        
        # Criação de alguns livros para o catálogo
        self.livro0 = Livro(0, "Química Orgânica", self.autor1, 2024, 1)
        self.livro1 = Livro(1, "Química Radical", self.autor1 , 2022, 2)
        self.livro2 = Livro(2, "Física Básica", self.autor2, 2021, 3)
        self.livro3 = Livro(1, "Astronomia",self.autor2, 2024,4)

        # Adicionando exemplares ao catálogo
        for livro in [self.livro1, self.livro2, self.livro3]:
            for id in range(3):
                copia = Livro(id, livro.titulo, livro.autores, livro.ano, livro.ISBN)
                self.biblioteca.adicionar_livro(copia)

        # Criação de um usuário para os testes
        self.usuario = Usuario(101, "Lucas", "apapa@example.com")
        self.biblioteca.cadastrar_usuario(self.usuario)

    def test_adicionar_livro(self):
        novo_livro = Livro(3, "Introdução à Biologia", self.autor2, 2023, 4)
        self.biblioteca.adicionar_livro(novo_livro)
        self.assertIn(novo_livro, self.biblioteca.catalogo[novo_livro.ISBN])

    def test_emprestar_livro_sucesso(self):
    
        self.assertTrue(self.biblioteca.emprestar_livro(self.livro1, self.usuario, datetime(2024, 6, 18)))
        self.assertTrue(self.livro1.esta_emprestado())

    def test_emprestar_livro_id0(self):
        self.assertFalse(self.biblioteca.emprestar_livro(self.livro0, self.usuario, datetime(2024, 6, 18)))

    def test_emprestar_livro_com_penalidade(self):
        self.biblioteca.emprestar_livro(self.livro1, self.usuario, datetime(2022,10,1)) #prazo maximo de 7 dias para devolucao
        self.biblioteca.devolver_livro(self.livro1, datetime(2022,10,10)) #devolve 10 dias depois
        self.assertFalse(self.biblioteca.emprestar_livro(self.livro2, self.usuario, datetime(2022, 10, 18)))

    def test_devolver_livro(self):
        livro_emprestado = self.livro1
        self.biblioteca.emprestar_livro(livro_emprestado, self.usuario, datetime(2024, 6, 18))
        self.biblioteca.devolver_livro(livro_emprestado, datetime(2024, 6, 25))
        self.assertFalse(livro_emprestado.esta_emprestado())
        self.assertIsNone(self.usuario.data_ultima_penalidade)

    def test_devolver_livro_com_atraso(self):
        livro_emprestado = self.livro1
        self.biblioteca.emprestar_livro(livro_emprestado, self.usuario, datetime(2024, 6, 18))
        self.biblioteca.devolver_livro(livro_emprestado, datetime(2024, 7, 2))
        self.assertTrue(self.usuario.possui_penalidade(datetime(2024, 7, 2)))

if __name__ == '__main__':
    unittest.main()
