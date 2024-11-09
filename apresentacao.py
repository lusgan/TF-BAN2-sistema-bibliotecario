# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:28:31 2024

@author: balbi
"""

import biblioteca_com_teste_unitario
import DAO
#Funcionalidades:
#1-Cadastrar bibliotecario
#2-cadastrar assistente
#3-cadastrar usuario
#4-cadastrar livro
#5-cadastrar exemplar
#6-realizar emprestimo
#7-localizar exemplar 
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
    print("8- Renovar empestimo")
    print("9 - Comandos do desenvolvedor")
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
        
        bibliotechman = biblioteca_com_teste_unitario.Bibliotecario(cpf, nome, rua, cidade, cep, telefone, endereco)
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
        
        assistente = biblioteca_com_teste_unitario.Assistente(cpf, nome, rua, cidade, cep, telefone, endereco, supervisores)
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
        
        
        usuario = biblioteca_com_teste_unitario.Usuario(cpf, nome, rua, cidade, cep, telefone, endereco, multa, categoria)
        DAO.cadastrar_usuario(usuario)

    
    #cadastrar livro
    elif escolha==4:
        titulo = input("titulo:")
        autores = input("autores separado por virgula:")
        autores = autores.split(",")
        ISBN = input("ISBN:")
        editora = input("editora:")
        colecao = input("colecao:")
        
        livro = biblioteca_com_teste_unitario.Livro(titulo, autores, ISBN, editora, colecao)
        DAO.cadastrar_livro(livro)

    
    #cadastrar exemplar
    elif escolha == 5:
        ISBN = input("ISBN:")
        
        if not DAO.verificar_isbn(ISBN):
            print("O ISBN não foi encontrado no banco de dados.\n")
            
        else:
        
            num = int(input("Numero do exemplar:"))
            status  = int(input("Status do exemplar:\n1- Disponivel\n2- Indisponivel\n"))
            
            if status == 1:
                status = 'Disponivel'
            
            elif status==2:
                status = 'Indisponivel'
            
            exemplar = biblioteca_com_teste_unitario.Exemplar(num, status)
            DAO.cadastrar_exemplar(exemplar,ISBN)








    
    elif escolha == 9: #opcoes de visualizacao
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
            
            
        
            




