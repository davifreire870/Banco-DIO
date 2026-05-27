from funcoes import *

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class BancoApp:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def menu(self):
        return input("""
------------- BANCO -------------
[1] Novo cliente
[2] Nova conta
[3] Depositar
[4] Sacar
[5] Extrato
[6] Listar contas
[0] Sair
Digite aqui: """).strip()

    def executar(self):
        while True:
            opcao = self.menu()

            if opcao == "1":
                self.criar_cliente()
            elif opcao == "2":
                self.criar_conta()
            elif opcao == "3":
                self.depositar()
            elif opcao == "4":
                self.sacar()
            elif opcao == "5":
                self.exibir_extrato()
            elif opcao == "6":
                self.listar_contas()
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opcao invalida.")

    def buscar_cliente_por_cpf(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente

        return None

    def selecionar_cliente(self):
        cpf = input("CPF do cliente: ").strip()
        cliente = self.buscar_cliente_por_cpf(cpf)

        if not cliente:
            print("Cliente nao encontrado.")

        return cliente

    def selecionar_conta(self, cliente):
        if not cliente.contas:
            print("Cliente nao possui conta.")
            return None

        if len(cliente.contas) == 1:
            return cliente.contas[0]

        for conta in cliente.contas:
            print(f"Conta: {conta.numero} | Agencia: {conta.agencia} | Saldo: R$ {conta.saldo:.2f}")

        numero = input("Numero da conta: ").strip()

        for conta in cliente.contas:
            if str(conta.numero) == numero:
                return conta

        print("Conta nao encontrada.")
        return None

    def ler_valor(self, mensagem):
        try:
            valor = float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Valor invalido.")
            return None

        if valor <= 0:
            print("O valor deve ser maior que zero.")
            return None

        return valor

    def criar_cliente(self):
        cpf = input("CPF: ").strip()

        if self.buscar_cliente_por_cpf(cpf):
            print("Cliente ja cadastrado.")
            return

        nome = input("Nome: ").strip()
        data_nascimento = input("Data de nascimento: ").strip()
        endereco = input("Endereco: ").strip()

        cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
        self.clientes.append(cliente)

        print("Cliente criado com sucesso.")

    def criar_conta(self):
        cliente = self.selecionar_cliente()

        if not cliente:
            return

        numero = len(self.contas) + 1
        conta = ContaCorrente.nova_conta(cliente, numero)
        self.contas.append(conta)
        cliente.adicionar_contas(conta)

        print(f"Conta {conta.numero} criada com sucesso.")

    def depositar(self):
        cliente = self.selecionar_cliente()

        if not cliente:
            return

        conta = self.selecionar_conta(cliente)

        if not conta:
            return

        valor = self.ler_valor("Valor do deposito: ")

        if valor is None:
            return

        transacao = deposito(valor)
        cliente.realizar_transacao(conta, transacao)

        print("Deposito realizado com sucesso.")

    def sacar(self):
        cliente = self.selecionar_cliente()

        if not cliente:
            return

        conta = self.selecionar_conta(cliente)

        if not conta:
            return

        valor = self.ler_valor("Valor do saque: ")

        if valor is None:
            return

        if valor > conta.saldo:
            print("Saldo insuficiente.")
            return

        transacao = saque(valor)
        cliente.realizar_transacao(conta, transacao)

        print("Saque realizado com sucesso.")

    def exibir_extrato(self):
        cliente = self.selecionar_cliente()

        if not cliente:
            return

        conta = self.selecionar_conta(cliente)

        if not conta:
            return

        print("\n========== EXTRATO ==========")

        if not conta.historico.transacoes:
            print("Nao foram realizadas movimentacoes.")

        for transacao in conta.historico.transacoes:
            tipo = transacao.__class__.__name__.capitalize()
            print(f"{tipo}: R$ {transacao.valor:.2f}")

        print(f"Saldo atual: R$ {conta.saldo:.2f}")
        print("=============================")

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return

        for conta in self.contas:
            print(f"Agencia: {conta.agencia} | Conta: {conta.numero} | Cliente: {conta.cliente.nome} | Saldo: R$ {conta.saldo:.2f}")


app = BancoApp()
app.executar()
