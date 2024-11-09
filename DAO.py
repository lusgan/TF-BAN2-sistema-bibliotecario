from pymongo import MongoClient

# Conecte-se ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['biblioteca']  # Nome do banco de dados


# Obtenha a coleção de bibliotecários
#ibliotecarios = db.bibliotecarios.find({}, {"nome": 1, "_id": 0})  # Seleciona apenas o campo "nome"

'''# Imprima o nome de cada bibliotecário
print("Nomes dos Bibliotecários:")
for bibliotecario in bibliotecarios:
    print(bibliotecario["nome"])
'''

def cadastrar_bibliotecario(bibliotecario):
    resultado = db.bibliotecarios.insert_one(bibliotecario.to_json())
    print("\nBibliotecário cadastrado com ID:", resultado.inserted_id)
    print("\n")
    
def get_bibliotecarios():
    return db.bibliotecarios.find()


def cadastrar_assistente(assistente):
    resultado = db.assistentes.insert_one(assistente.to_json())
    print("\nAssistente cadastrado com ID:", resultado.inserted_id)
    print("\n")
    
def get_assistentes():
    return db.assistentes.find()


def cadastrar_usuario(usuario):
    resultado = db.usuarios.insert_one(usuario.to_json())
    print("\nUsuario cadastrado com ID:", resultado.inserted_id)
    print("\n")
    
def get_usuarios():
    return db.usuarios.find()


def cadastrar_livro(livro):
    resultado = db.livros.insert_one(livro.to_json())
    print("\nLivro cadastrado com ID:", resultado.inserted_id)
    print("\n")

def get_livros():
    return db.livros.find()


def cadastrar_exemplar(exemplar,ISBN):
    # Atualizar o livro pelo ISBN, adicionando o novo exemplar ao array "Exemplares"
    db.livros.update_one(
        {"ISBN": ISBN},   # Filtro: ISBN do livro desejado
        {"$push": {"Exemplares": exemplar.to_json()}}  # Adiciona o exemplar ao array "Exemplares"
    )
    
def get_exemplares(ISBN):
    return db.exemplares.find()

def verificar_isbn(isbn):
    livro = db.livros.find_one({"ISBN": isbn})
    if livro:
        return True
    else:
        return False