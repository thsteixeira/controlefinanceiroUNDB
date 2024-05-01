import sqlite3
import os
from datetime import datetime

class Transacao:
    """
    Classe para representar uma transação financeira.
    """
    def __init__(self, data, valor, tipo, categoria, descricao):
        """
        Inicializa uma nova transação com os dados fornecidos.
        """
        self.data = data
        self.valor = valor
        self.tipo = tipo  # 'despesa' ou 'receita'
        self.categoria = categoria
        self.descricao = descricao

class GerenciadorFinanceiro:
    """
    Classe para gerenciar transações financeiras.
    """
    def __init__(self):
        """Inicializa o gerenciador e cria o Banco de Dados caso ele ainda não exista"""
        if not os.path.isfile("transacoes.db"):
            self.con = sqlite3.connect("transacoes.db")
            self.cur = self.con.cursor()
            self.cur.execute("CREATE TABLE transacoes(id integer PRIMARY KEY, data TIMESTAMP NOT NULL, valor real NOT NULL, tipo NOT NULL, categoria, descricao)")
        else:
            self.con = sqlite3.connect("transacoes.db")
            self.cur = self.con.cursor()
        print("Banco de dados criado com sucesso!")

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma nova transação à lista de transações.
        """
        self.cur.execute("INSERT INTO transacoes(data, valor, tipo, categoria, descricao) VALUES (?, ?, ?, ?, ?)", (transacao.data, transacao.valor, transacao.tipo, transacao.categoria, transacao.descricao) )
        self.con.commit()

    def verificar_saldo(self):
        """
        Calcula o saldo total com base nas transações registradas.
        """
        self.cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo='receita'")
        receitas = self.cur.fetchone()[0]
        if receitas == None : receitas = 0
        self.cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo='despesa'")
        despesas = self.cur.fetchone()[0]
        if despesas == None : despesas = 0
        saldo = receitas - despesas
        return saldo

    def relatorio_transacoes_por_categoria(self):
        """
        Gera um relatório de transacoes por categoria.
        """
        self.cur.execute("SELECT DISTINCT categoria FROM transacoes")
        categorias = self.cur.fetchall()
        print("### Relatório de Transações por Categoria ###")
        for categoria in categorias:
            self.cur.execute("SELECT SUM(valor) FROM transacoes WHERE categoria = (?)", categoria)
            total_gasto = self.cur.fetchone()[0]
            print(f'{categoria[0].capitalize()}: R$ {total_gasto:.2f}')

    def consultar_transacoes_por_data(self, data):
        """
        Consulta as transações realizadas em uma data específica.
        """
        data = datetime.strptime(data, "%d-%m-%Y")
        self.cur.execute("SELECT * FROM transacoes WHERE data = ?", (data,))
        transacoes_data = self.cur.fetchall()
        return transacoes_data

    def estatisticas_financeiras(self):
        """
        Calcula as estatísticas financeiras, como média de despesas e receitas.
        """
        self.cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'")
        receitas = self.cur.fetchone()[0]
        self.cur.execute("SELECT Count() FROM transacoes WHERE tipo = 'receita'")
        qntreceitas = self.cur.fetchone()[0]
        #print(receitas, qntreceitas)
        media_receitas = receitas/qntreceitas
        
        self.cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'despesa'")
        despesas = self.cur.fetchone()[0]
        self.cur.execute("SELECT Count() FROM transacoes WHERE tipo = 'despesa'")
        qntdespesas = self.cur.fetchone()[0]
        #print(despesas, qntdespesas)
        media_despesas = despesas/qntdespesas
        
        return media_despesas, media_receitas

def exibir_menu():
    """
    Exibe o menu de opções para o usuário.
    """
    print("\n### Menu ###")
    print("1. Adicionar transação")
    print("2. Verificar saldo")
    print("3. Relatório por categoria")
    print("4. Consultar transações por data")
    print("5. Estatísticas financeiras")
    print("0. Sair")


def main():
    """
    Função principal para executar o sistema de gerenciamento financeiro.
    """
    gerenciador = GerenciadorFinanceiro()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            data = input("Digite a data (DD-MM-YYYY): ")
            data = datetime.strptime(data, "%d-%m-%Y")
            valor = float(input("Digite o valor: "))
            numtipo = int(input("Digite o tipo: \n1 para receita ou \n2 para despesa "))
            match numtipo:
                case 1:
                    tipo = "receita"
                    numcategoria = int(input("Digite a categoria: \n1 para salário \n2 para dividendos \n3 para outras receitas "))
                    match numcategoria:
                        case 1:
                           categoria = "salário"
                        case 2:
                            categoria = "dividendos"
                        case 3:
                            categoria = "outras receitas"
                case 2:
                    tipo = "despesa"
                    numcategoria = int(input("Digite a categoria: \n1 para educação \n2 para alimentação \n3 para moradia \n4 para transporte \n5 para outras despesas "))
                    match numcategoria:
                        case 1:
                           categoria = "educação"
                        case 2:
                            categoria = "alimentação"
                        case 3:
                            categoria = "moradia"
                        case 4:
                            categoria = "transporte"
                        case 5:
                            categoria = "outras despesas"
            descricao = input("Digite uma descrição: ")
            transacao = Transacao(data, valor, tipo, categoria, descricao)
            gerenciador.adicionar_transacao(transacao)
            print("Transação adicionada com sucesso!")

        elif opcao == '2':
            saldo = gerenciador.verificar_saldo()
            print(f"Saldo atual: R$ {saldo:.2f}")

        elif opcao == '3':
            gerenciador.relatorio_transacoes_por_categoria()

        elif opcao == '4':
            data = input("Digite a data (DD-MM-YYYY): ")
            transacoes_data = gerenciador.consultar_transacoes_por_data(data)
            if transacoes_data:
                print(f"Transações em {data}:")
                for transacao in transacoes_data:
                    print(f"{transacao[1]}: {transacao[3]} - R$ {transacao[2]:.2f} ({transacao[4]}) - {transacao[5]}")
            else:
                print("Nenhuma transação encontrada para esta data.")

        elif opcao == '5':
            media_despesas, media_receitas = gerenciador.estatisticas_financeiras()
            print("Estatísticas financeiras:")
            print(f"Média de despesas: R$ {media_despesas:.2f}")
            print(f"Média de receitas: R$ {media_receitas:.2f}")

        elif opcao == '0':
            print("Saindo do programa...")
            gerenciador.con.close()
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
