import os
import sys
from typing import Optional
import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'tp_01'
}

class TP01CLI:
    def __init__(self):
        self.conexao = None
        print("TP01 - CLI Inicializado")

    def conectar_banco(self):
        try:
            self.conexao = psycopg2.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            
            print("Conectando ao banco PostgreSQL...")
            #self.conexao = psycopg2.connect(**pg_config)
            self.conexao.autocommit = True
            print("Conexão estabelecida com sucesso!")
            return True
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False
        return True
    
    def desconectar_banco(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados encerrada.")
    
    def executar_consulta(self, sql: str, descricao: str) -> None:
        """Executa uma consulta SQL e exibe os resultados formatados"""
        print(f"\nExecutando: {descricao}")
        print("=" * 60)
        print(f"SQL: {sql.strip()}")
        print("=" * 60)
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            
            if resultados:
                # Exibir cabeçalhos
                print("\n Resultados:")
                
                header = " | ".join(f"{col:<20}" for col in colunas)
                print(header)
                print("-" * len(header))
                
                # Exibir dados
                for linha in resultados:
                    row = " | ".join(f"{str(valor):<20}" for valor in linha)
                    
                    print(row)
                    
                print(f"\nTotal de registros encontrados: {len(resultados)}")
                
            else:
                print("\nNenhum registro encontrado.")
                
        except psycopg2.Error as e:
            print(f"\nErro na consulta SQL: {e}")
        except Exception as e:
            print(f"\nErro inesperado: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
        
        print("\nConsulta finalizada!")

    def exemplo(self):
        """Exemplo de consulta SQL"""
        sql = "SELECT * FROM sua_tabela WHERE condicao = 'valor'"
        self.executar_consulta(sql, "Consulta de Exemplo")

    def menu(self):
        while True:
            print("\nMenu de Consultas:")
            print("1. Exemplo de Consulta")
            print("2. Sair")
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.exemplo()
            elif opcao == '2':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")

def main():
    cli = TP01CLI()
    if cli.conectar_banco():
        try:
            cli.menu()
        finally:
            cli.desconectar_banco()
    else:
        print("Não foi possível conectar ao banco de dados. Encerrando o programa.")

if __name__ == "__main__":
    main()