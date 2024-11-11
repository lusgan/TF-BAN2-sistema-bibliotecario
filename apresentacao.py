# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:28:31 2024

@author: balbi
"""

import biblioteca_camada_logica
import DAO
import datetime
#Funcionalidades:
#1-Cadastrar bibliotecario
#2-cadastrar assistente
#3-cadastrar usuario
#4-cadastrar livro
#5-cadastrar exemplar
#6-realizar emprestimo
#7-Devolução de livro
#7-localizar exemplar   PARA ESSE JA CRIEI A FUNCAO DAO.GET_EXEMPLAR()
#8-renovar emprestimo

def menu():
    print("Menu:")
    print("1- Cadastrar bibliotecario")
    print("2- Cadastrar asssistente")
    print("3- Cadastrar usuario")
    print("4- Cadastrar livro")
    print("5- Cadastrar exemplar")
    print("6- Realizar emprestimo")
    print("7- Localizar exemplar")
    print("8- Devolucao de exemplar")
    print("9- Renovar emprestimo")
    print("10 - Comandos do desenvolvedor")
    print("0- Sair\n")
    
    opcao = int(input())
    return opcao


def menu_do_desenvolvedor():
    print("Menu dev:")
    print("1- visualizar bibliotecarios")
    print("2- visualizar asssistentes")
    print("3- visualizar usuarios")
    print("4- visualizar livros")
    print("5- visualizar exemplares")
    print("6- visualizar emprestimos")
    print("0- voltar\n")
    
    opcao = int(input())
    return opcao


escolha = 1

while escolha!= 0 :
    
    escolha = menu()
    
    #cadastrar bibliotecario
    if escolha == 1:
        cpf = input("CPF:")
        nome = input("Nome:")
        rua = input("Rua:")
        cidade = input("Cidade:")
        cep = input("Cep:")
        telefone = input("Telefone:")
        endereco = input("Endereco:")
        
        bibliotechman = biblioteca_camada_logica.Bibliotecario(cpf, nome, rua, cidade, cep, telefone, endereco)
        DAO.cadastrar_bibliotecario(bibliotechman)
   
    
   
        
        ''' FALTA COLOCAR AS CONDICOES DE ERRO PARA O CADASTRO DE ASSISTENTE
        Exemplo: Nos casos em que o supervisor nao existe, ou caso nao seja passado nada como supervisor'''
     #cadastrar assistente:
    elif escolha == 2:
        cpf = input("CPF:")
        nome = input("Nome:")
        rua = input("Rua:")
        cidade = input("Cidade:")
        cep = input("Cep:")
        telefone = input("Telefone:")
        endereco = input("Endereco:")
        supervisores = input("CPF dos supervisores separado por virgula:")
        supervisores = supervisores.split(",")
        
        assistente = biblioteca_camada_logica.Assistente(cpf, nome, rua, cidade, cep, telefone, endereco, supervisores)
        DAO.cadastrar_assistente(assistente)
        
    
    
    #cadastrar usuario
    elif escolha == 3:   
        cpf = input("CPF:")
        nome = input("Nome:")
        rua = input("Rua:")
        cidade = input("Cidade:")
        cep = input("Cep:")
        telefone = input("Telefone:")
        endereco = input("Endereco:")
        multa = 0
        
        
        categoria_int = int(input("Qual categoria?\n1- Aluno de graduacao\n2- Aluno de pos-graduacao\n3- Professor\n4- Professor de pos-graduacao\n"))
        categoria = 'erro'
        
        if categoria_int == 1:
            categoria = {'id':1, 'Categoria':'Aluno de graduacao'}
            
        elif categoria_int==2:
            categoria = {'id':2, 'Categoria': "Aluno de pos-graduacao"}
            
        elif categoria_int == 3:
            categoria = {'id' : 3, 'categoria' : 'Professor'}
            
        elif categoria_int==4:
            categoria = {'id': 4, 'categoria' :"Professor de pos-graduacao"}
        
        
        usuario = biblioteca_camada_logica.Usuario(cpf, nome, rua, cidade, cep, telefone, endereco, multa, categoria)
        DAO.cadastrar_usuario(usuario)

    
    #cadastrar livro
    elif escolha==4:
        titulo = input("titulo:")
        autores = input("autores separado por virgula:")
        autores = autores.split(",")
        ISBN = input("ISBN:")
        editora = input("editora:")
        colecao = input("colecao:")
        
        livro = biblioteca_camada_logica.Livro(titulo, autores, ISBN, editora, colecao)
        DAO.cadastrar_livro(livro)

    
    #cadastrar exemplar
    elif escolha == 5:
        ISBN = input("ISBN:")
        
        if not DAO.verificar_isbn(ISBN):
            print("O ISBN não foi encontrado no banco de dados.\n")
            
        else:
        
            num = int(input("Numero do exemplar:"))
            
            if DAO.get_exemplar(ISBN, num):
                print("Exemplar com esse numero ja está cadastrado!")
            
            else:
                status  = int(input("Status do exemplar:\n1- Disponivel\n2- Indisponivel\n"))
                
                if status == 1:
                    status = 'Disponivel'
                
                elif status==2:
                    status = 'Indisponivel'
                
                exemplar = biblioteca_camada_logica.Exemplar(num, status)
                DAO.cadastrar_exemplar(exemplar,ISBN)


    
    #realizar emprestimo
    elif escolha == 6:
        
        data_hoje = datetime.date.today()
        ISBN = input("ISBN:")
        num_exemplar = int(input("Exemplar:"))
        CPF = input("CPF:")
        
        usuario = DAO.get_usuario(CPF)
        if not usuario:
            print("usuario nao encontrado")
        
        else:
            categoria = usuario['Categoria']['Categoria']
            qtd_dias = "erro"
            
            if categoria == "Aluno de graduacao":
                qtd_dias = 15
            
            elif categoria == "Aluno de pos-graduacao":
                qtd_dias = 30
            
            elif categoria == "Professor":
                qtd_dias = 30
                
            elif categoria == "Professor de pos-graduacao":
                qtd_dias = 90
            
            data_hoje = input("data de hoje (DD-MM-YYYY):")
            data_hoje = datetime.datetime.strptime(data_hoje, "%d-%m-%Y").date()
            
            emprestimo = biblioteca_camada_logica.Emprestimo(data_hoje, ISBN, num_exemplar, CPF, qtd_dias)
            biblioteca_camada_logica.emprestar_livro(emprestimo,data_hoje)
            
    
    #localizar exemplar
    elif escolha == 7:
        ISBN = input("ISBN:")
        numero = int(input("numero:"))
        exemplar = DAO.get_exemplar(ISBN, numero)
        print(exemplar)
        
    
    #devolver exemplar
    elif escolha == 8:
        ISBN = input("ISBN:")
        num_exemplar = int(input("Exemplar:"))
        data_devolucao = input("Data da devolucao (DD-MM-YYYY):")
        
        data_devolucao = datetime.datetime.strptime(data_devolucao, "%d-%m-%Y").date()
        
        biblioteca_camada_logica.devolver_livro(ISBN, num_exemplar, data_devolucao)

    
    #renovar emprestimo
    elif escolha == 9:
        
        ISBN = input('ISBN:')
        num_exemplar = int(input("Exemplar:"))
        data_hoje = input("data de hoje (DD-MM-YYYY):")
        data_hoje = datetime.datetime.strptime(data_hoje, "%d-%m-%Y").date()
        biblioteca_camada_logica.renovar_emprestimo(ISBN, num_exemplar, data_hoje)



    
    elif escolha == 10: #opcoes de visualizacao
        opcao = menu_do_desenvolvedor()
        
        #visualizar bibliotecarios
        if opcao == 1:
            bibliotecarios = DAO.get_bibliotecarios()
            
            for b in bibliotecarios:
                print(b)
                print("\n")
                
        
        #visualizar assistentes
        elif opcao==2:
            assistentes = DAO.get_assistentes()
            
            for a in assistentes:
                print(a)
                print("\n")
        
        
        #visualizar usuarios
        elif opcao==3:
            usuarios = DAO.get_usuarios()
            
            for u in usuarios:
                print(u)
                print("\n")
        
        
        #visualizar livros
        elif opcao==4:
            livros = DAO.get_livros()
            
            for l in livros:
                print(l)
                print("\n")
        
        
        #visualizar exemplares
        elif opcao==5:
            ISBN = input("ISBN:")
            exemplares = DAO.get_exemplares(ISBN)
            
            for e in exemplares:
                print(e)
                print("\n")
        
        
        elif opcao==6 :
            emprestimos = DAO.get_todos_emprestimos()
            
            for e in emprestimos:
                print(e)
                print("\n")
            
        
            




