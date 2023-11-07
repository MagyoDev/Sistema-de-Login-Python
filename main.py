from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from database import *

Window.size = (350, 580)

class LimaAPP(MDApp):
    None

    def build(self):
        self.theme_cls.primary_palette = "Red"
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("screens/cadastrar.kv"))
        sm.add_widget(Builder.load_file("screens/opcoes_conta.kv"))
        sm.add_widget(Builder.load_file("screens/listar.kv"))
        sm.add_widget(Builder.load_file("screens/detalhes_conta.kv"))
        sm.add_widget(Builder.load_file("screens/atualizar_info.kv"))
        sm.add_widget(Builder.load_file("screens/aluno.kv"))
        sm.add_widget(Builder.load_file("screens/professor.kv"))
        sm.add_widget(Builder.load_file("screens/logar.kv"))
        return sm

    def cadastrar(self, nome, email, senha):
        # Função para criar uma nova conta
        criar_conta('secretaria', nome, email, senha)
        tela_cadastro = self.root.get_screen("cadastrar")  # Obtém a referência à tela de cadastro
        tela_cadastro.ids.nome_field.text = "" # Limpa o campo de nome
        tela_cadastro.ids.email_field.text = ""  # Limpa o campo de e-mail
        tela_cadastro.ids.senha_field.text = ""  # Limpa o campo de senha
        self.root.current = "logar"  # Volta para a tela de login

    def login_conta(self, email, senha):
        # Função para fazer login
        dominios_permitidos = ["secretaria.com", "professor.com", "aluno.com"]
        partes_email = email.split('@')

        if len(partes_email) == 2 and partes_email[1] in dominios_permitidos:
            contas = db.reference('contas').order_by_child('email').equal_to(email).get()
            if contas:
                for _, info in contas.items():
                    if info.get('senha') == senha and info.get('validada', False):
                        print("Login bem-sucedido.")
                        if partes_email[1] == "secretaria.com":
                            self.root.current = "opcoes_conta"  
                        elif partes_email[1] == "professor.com":
                            self.root.current = "professor"  
                        elif partes_email[1] == "aluno.com":
                            self.root.current = "aluno"  
                        else:
                            print("Domínio inválido.")
                    elif info.get('senha') == senha and not info.get('validada', False):
                        print("Conta não validada.")
                    else:
                        print("Senha incorreta.")
            else:
                print("Conta não encontrada.")
        else:
            print("E-mail com domínio inválido. Use um e-mail válido.")

    def validar_conta(self, email):
        # Função para validar uma conta
        contas_ref = db.reference('contas').order_by_child('email').equal_to(email).get()

        if contas_ref:
            for key, conta in contas_ref.items():
                if not conta.get('validada', False):
                    db.reference(f'contas/{key}/validada').set(True)
                    db.reference(f'contas/{key}/status').set('ativo') 
                    print(f"A conta de {conta['email']} foi validada com sucesso e está ativa.")
                else:
                    print("Esta conta já está validada.")
        else:
            print("Conta não encontrada.")

    def inativar_conta(self, email):
        # Função para inativar uma conta
        contas_ref = db.reference('contas').order_by_child('email').equal_to(email).get()

        if contas_ref:
            for key in contas_ref:
                conta = contas_ref[key]
                db.reference(f'contas/{key}/status').set('inativo')
                db.reference(f'contas/{key}/validada').set(False) 
                print(f"A conta de {conta['email']} foi inativada com sucesso.")
        else:
            print("Conta não encontrada.")

    def carregar_contas(self):
        # Função para carregar a lista de contas
        contas = listar_contas()
        account_list = self.root.get_screen("listar").ids.account_list
        account_list.clear_widgets()

        for conta in contas:
            item = OneLineListItem(text=f"{conta['nome']}: {conta['email']}")
            item.bind(on_release=lambda item: self.abrir_detalhes_conta(item.text))
            account_list.add_widget(item)

    def abrir_detalhes_conta(self, text):
        # Função para abrir os detalhes de uma conta
        nome, email = text.split(": ")
        detalhes_conta = self.root.get_screen("detalhes_conta")
        detalhes_conta.ids.nome_conta.text = nome
        detalhes_conta.ids.email_conta.text = email
        self.root.current = "detalhes_conta"

    def atualizar_conta(self, nome, email, senha, novo_email, nova_senha):
        # Função para atualizar as informações de uma conta
        conta_ref = db.reference('contas')
        contas = conta_ref.order_by_child('email').equal_to(email).get()

        if contas:
            for conta_id, info in contas.items():
                conta_ref.child(conta_id).update({'nome': nome, 'email': novo_email, 'senha': nova_senha})
                print(f"Informações da conta de {email} atualizadas com sucesso.")
        else:
            print("Conta não encontrada.")

if __name__ == "__main__":
    LimaAPP().run()