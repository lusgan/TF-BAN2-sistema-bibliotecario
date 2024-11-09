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
    return db.livros.find({"ISBN" : ISBN})

def get_exemplar(ISBN, numero):
    # Realiza a busca do livro pelo ISBN e procura por um exemplar com o número especificado
    livro = db.livros.find_one(
        {
            "ISBN": ISBN,
            "Exemplares.num": numero  # Procura pelo número do exemplar dentro da lista
        }
    )

    if livro:
        # Percorre a lista de exemplares para encontrar o exemplar correto
        for exemplar in livro['Exemplares']:
            if exemplar['num'] == numero:
                return exemplar  # Retorna o exemplar encontrado

    return None  # Caso não encontre o exemplar


def verificar_isbn(isbn):
    livro = db.livros.find_one({"ISBN": isbn})
    if livro:
        return True
    else:
        return False
    


def atualizar_exemplar(ISBN, numero, novo_status, nova_posse):
    resultado = db.livros.update_one(
    {
        "ISBN": ISBN,
        "Exemplares.num": numero  
    },
    {
        "$set": {
            "Exemplares.$.status": novo_status,
            "Exemplares.$.posse": nova_posse
        }
    }
)
    

def adicionar_emprestimo_usuario(emprestimo):
  
    db.emprestimos.insert_one(emprestimo.to_json())

    
    resultado = db.usuarios.update_one(
        {"CPF": emprestimo.CPF},
        {"$push": {"emprestimos": emprestimo.to_json()}}
    )

    if resultado.matched_count > 0:
        print("Empréstimo adicionado com sucesso ao usuário.")
    else:
        print("Usuário não encontrado.")



def get_id_ultimo_emprestimo():
    ultimo_emprestimo = db.emprestimos.find_one({}, sort = [('_id', -1)])
    
    if not ultimo_emprestimo:
        return 0
    
    else :
        return ultimo_emprestimo['id']
    

def get_usuario(CPF):
    return db.usuarios.find_one({"CPF": CPF})
