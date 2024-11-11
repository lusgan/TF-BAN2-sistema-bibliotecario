from pymongo import MongoClient

# Conecte-se ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['biblioteca']  # Nome do banco de dados



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
        {"$push": {"Emprestimos": emprestimo.to_json()}}
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


def get_emprestimo(ISBN, exemplar):
    return db.emprestimos.find_one({"ISBN": ISBN, "Exemplar": exemplar}, {'_id': 0})


def atualizar_emprestimo(ISBN, exemplar, data_devolucao, multa, renovacoes, Fim):
    resultado = db.emprestimos.update_one(
        {"ISBN": ISBN, "Exemplar": exemplar},  # Filtro para encontrar o empréstimo
        {
            "$set": {
                "Fim" : Fim,
                "Data de devolucao": data_devolucao,  # Atualizar a data de devolução
                "Multa": multa,  # Atualizar o valor da multa
                "Renovacoes" : renovacoes
            }
        }
    )
    
    # Verifica se o empréstimo foi encontrado e atualizado
    if resultado.matched_count > 0:
        print("Empréstimo atualizado com sucesso!")
    else:
        print("Empréstimo não encontrado.")
        


def get_colecao(ISBN):
    # Realiza a consulta no MongoDB para encontrar o livro com o ISBN fornecido
    livro = db.livros.find_one(
        {"ISBN": ISBN},  # Filtro para encontrar o livro com o ISBN
        {"Colecao": 1, "_id": 0}  # Projeção para retornar apenas o campo Colecao
    )
    
    # Verifica se o livro foi encontrado
    if livro:
        return livro.get('Colecao', None)  # Retorna o valor de 'Colecao', ou None se não existir
    else:
        return None  # Retorna None se o livro não for encontrado



def apagar_emprestimo_usuario(CPF, emprestimo_id, multa):
    # Remove o empréstimo com base no CPF e no ID do empréstimo
    resultado = db.usuarios.update_one(
        {"CPF": CPF},  # Filtro para encontrar o usuário pelo CPF
        {
            "$pull": {  # Remove o empréstimo com o ID especificado
                "Emprestimos": {"id": emprestimo_id}
            },
            "$set": {  # Atualiza o campo de multa, se aplicável
                "Multa": multa
            }
        }
    )
    
    
def get_todos_emprestimos():
    return db.emprestimos.find()


def atualizar_emprestimo_em_usuario(CPF, id_emprestimo, renovacoes, Fim):
    db.usuarios.update_one(
        {"CPF": CPF, "Emprestimos.id": id_emprestimo},
        {
            "$set": {
                "Emprestimos.$[emprestimo].Renovacoes": renovacoes,
                "Emprestimos.$[emprestimo].Fim": Fim
            }
        },
        array_filters=[{"emprestimo.id": id_emprestimo}]
    )
