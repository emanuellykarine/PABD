import os
import sys
import requests
import json

API_URL = "http://localhost:8000/api/"

class ProjetoTarefaCliente:
    def __init__(self):
        self.token = None
        self.user = None
        print("Cliente Projeto e Tarefa Inicializado")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        
        data = {
            'username': username, 
            'password': password
            }
        
        response = requests.post(f"{API_URL}login/", json=data)

        if response.status_code == 200:
            resultado = response.json()
            self.token = resultado['token']
            self.user = resultado['user']
            print("Login bem-sucedido!")
        else:
            print(f"Falha no login (status {response.status_code}):")
            try:
                print(response.json())
            except:
                print(response.text)

    def signup(self):
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")

        data = {
            'username': username, 
            'password': password,
            'email': email
            }
        
        response = requests.post(f"{API_URL}signup/", json=data)

        if response.status_code == 200:
            print("Signup bem-sucedido!")
            self.token = response.json()['token']
            self.user = response.json()['user']
        else:
            print(f"Falha no signup (status {response.status_code}):")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print(response.text)

    def cadastrar_projeto(self):
        nome = input("Nome do Projeto: ")
        descricao = input("Descrição do Projeto: ")

        data = {
            'nome': nome, 
            'descricao': descricao
            }
        
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.post(f"{API_URL}projetos/", json=data, headers=headers)
        
        if response.status_code == 201:
            print("Projeto cadastrado com sucesso!")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Falha ao cadastrar projeto (status {response.status_code}):")
            try:
                print(response.json())
            except:
                print(response.text)

    def cadastrar_tarefa(self):
        projeto = input("Digite o id do projeto: ")
        titulo = input("Digite o titulo da tarefa: ")
        descricao = input("Digite a descrição da tarefa: ")

        data = {
            'projeto': projeto, 
            'titulo': titulo, 
            'descricao': descricao
            }
        
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.post(f"{API_URL}tarefas/", json=data, headers=headers)

        if response.status_code == 201:
            print("Tarefa cadastrada com sucesso!")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Falha ao cadastrar tarefa (status {response.status_code}):")
            try:
                print(response.json())
            except:
                print(response.text)

    def listar_tarefas(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(f"{API_URL}tarefas/", headers=headers)

        if response.status_code == 200:
            print("\n=== TAREFAS ===")
            tarefas = response.json()
            print(json.dumps(tarefas, indent=2, ensure_ascii=False))
            print(f"\nTotal: {len(tarefas)} tarefas")
        else:
            print("RESPOSTA (falha):")
            print(response.text) 
    
    def listar_projetos(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(f"{API_URL}projetos/", headers=headers)

        if response.status_code == 200:
            print("\n=== PROJETOS ===")
            projetos = response.json()
            print(json.dumps(projetos, indent=2, ensure_ascii=False))
            print(f"\nTotal: {len(projetos)} projetos")
        else:
            print("RESPOSTA (falha):")
            print(response.text) 

    def testar_token(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(f"{API_URL}test-token/", headers=headers)   

        if response.status_code == 200:
            print("Token válido:", response.text)
        else:
            print("Token inválido:", response.text)
            self.token = None
            self.user = None

    def menu(self):
        while True:
            print("\nMenu:")
            if self.token and self.user:
                print(f"Usuário: {self.user.get('username')}")
                print(f"Token: {self.token}")
                print("1. Listar Projetos")
                print("2. Listar Tarefas")
                print("3. Cadastrar projeto")
                print("4. Cadastrar tarefa")
                print("5. Sair")
            else:
                print("1. Login")
                print("2. Signup")
                print("3. Testar token")
                print("4. Sair")
            
            opcao = input("Escolha uma opção: ")
            if self.token and self.user:
                if opcao == '1':
                    self.listar_projetos()
                elif opcao == '2':
                    self.listar_tarefas()
                elif opcao == '3':
                    self.cadastrar_projeto()
                elif opcao == '4':
                    self.cadastrar_tarefa()
                elif opcao == '5':
                    print("Saindo...")
                    self.token = None
                    self.user = None
                    print("Sessão encerrada.")
                else:
                    print("Opção inválida. Tente novamente.")
            else:
                if opcao == '1':
                    self.login()
                elif opcao == '2':
                    self.signup()
                elif opcao == '3':
                    self.testar_token()
                elif opcao == '4':
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")

def main():
    cliente = ProjetoTarefaCliente()

    response = requests.get(API_URL)
    if response.status_code == 200:
        print("Conectado à API com sucesso!")
        cliente.menu()

if __name__ == "__main__":
    main()
