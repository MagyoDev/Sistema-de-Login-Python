from firebase_admin import credentials, db, initialize_app, auth

# Inicializa o aplicativo Firebase
cred = credentials.Certificate('banco-teste-f8b16-firebase-adminsdk-ga420-9bc3d22fb2.json')
initialize_app(cred, {
    'databaseURL': 'https://banco-teste-f8b16-default-rtdb.firebaseio.com/'
})

def verificar_dominio(email):
    # Verifica se o e-mail tem um domínio permitido
    dominios_permitidos = ["secretaria.com", "professor.com", "aluno.com"]
    partes_email = email.split('@')
    
    if len(partes_email) == 2 and partes_email[1] in dominios_permitidos:
        return True
    else:
        return False

# Funções da secretaria
def criar_conta(criador, nome, email, senha):
    # Cria uma nova conta (apenas a secretaria pode criar)
    dominios_permitidos = ["secretaria.com", "professor.com", "aluno.com"]
    partes_email = email.split('@')
    
    if len(partes_email) == 2 and partes_email[1] in dominios_permitidos:
        if criador == 'secretaria':
            # Cria a conta no banco de dados
            nova_conta = {
                'nome': nome,
                'email': email,
                'senha': senha,
                'status': 'ativo',  # Definindo a conta como ativa por padrão
                'validada': False
            }
            ref = db.reference('contas')
            ref.push(nova_conta)
            print(f"Conta cadastrada com sucesso.")
            return True, "Conta criada com sucesso."
        else:
            print("Apenas a secretaria pode cadastrar contas para alunos, professores ou ela mesma.")
            return False, "Apenas a secretaria pode criar contas."

def listar_contas():
    # Lista todas as contas de alunos e professores no sistema
    contas = db.reference('contas').get()
    lista_contas = []
    for _, info in contas.items():
        lista_contas.append({
            'nome': info['nome'],
            'email': info['email'],
            'senha': info['senha'],
        })
    return lista_contas