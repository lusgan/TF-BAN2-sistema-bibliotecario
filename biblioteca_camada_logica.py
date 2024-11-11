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
        self.emprestimos = []
        
    
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
        self.renovacoes = 0

    def devolver(self, data):
        self.livro.emprestado = False
        self.dia_que_foi_devolvido = data
        if data > self.dataFinal:
            self.usuario.penalizar(data, self)
    
    def to_json(self):
        
        json = {'id': self.id_emprestimo, 'Inicio' : self.dataInicial, 'Fim' : self.dataFinal, 'Data de devolucao' : self.dia_que_foi_devolvido, 'ISBN' : self.ISBN, 'Exemplar' : self.num_exemplar, 'CPF' : self.CPF, 'Multa' : self.multa, 'Renovacoes' : self.renovacoes}
        return json
 



def usuario_possui_atraso(CPF, data_hoje):
    
    usuario = DAO.get_usuario(CPF)    
    emprestimos = usuario['Emprestimos']

    if not emprestimos:
        return False
    
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
    
    if not exemplar:
        print("Exemplar nao cadastrado.")
    
    else:
        usuario = DAO.get_usuario(emprestimo.CPF)
        
        limite_de_emprestimos = 4
        emprestimos = usuario['Emprestimos']
        qtd_emprestimos = 0
        
        if(emprestimos):
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
    renovacoes = emprestimo['Renovacoes']
    
    if data_devolucao > datetime.datetime.strptime(emprestimo['Fim'], "%d-%m-%Y").date():
        multa = 30
    
    Fim = emprestimo["Fim"]
    DAO.atualizar_emprestimo(ISBN, num_exemplar, data_devolucao.strftime('%d-%m-%Y'), multa,renovacoes, Fim)  
    DAO.atualizar_exemplar(ISBN, num_exemplar, 'Disponivel', None)
    DAO.apagar_emprestimo_usuario(emprestimo['CPF'], emprestimo['id'], multa)
    

def renovar_emprestimo(ISBN, num_exemplar, data_hoje):
    
    emprestimo = DAO.get_emprestimo(ISBN, num_exemplar)
    multa = emprestimo['Multa']
    
    usuario = DAO.get_usuario(emprestimo['CPF'])
    categoria_id = usuario['Categoria']['id']
    
    tempo_em_dias = None
    
    if categoria_id == 1: #estudante de graduacao
        tempo_em_dias = 15
    
    elif categoria_id == 2: #estudante de pos
        tempo_em_dias = 30
    
    elif categoria_id == 3: #prof
        tempo_em_dias = 30
    
    elif categoria_id == 4: #prof graduacao
        tempo_em_dias = 90
        
    
    if data_hoje > datetime.datetime.strptime(emprestimo['Fim'], "%d-%m-%Y").date():
        print("Livro atrasado, nao pode ser renovado.")
    
    elif emprestimo['Renovacoes'] == 3 :
        print("Limite de renovacoes atingido.")
    
    elif emprestimo['Data de devolucao']:
        print("Livro ja foi devolvido, nao eh possivel renovar.")
    
    else:
        renovacoes = emprestimo['Renovacoes'] + 1
        data_devolucao = None
        Fim  = (data_hoje + timedelta(days = tempo_em_dias)).strftime("%d-%m-%Y")     
        DAO.atualizar_emprestimo(ISBN, num_exemplar, data_devolucao, multa, renovacoes, Fim)
        DAO.atualizar_emprestimo_em_usuario(usuario['CPF'], emprestimo['id'], renovacoes, Fim)


