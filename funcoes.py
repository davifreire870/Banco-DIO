from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_contas(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 300
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()


    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
    

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True

        return False
    
    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self._saldo -= valor
            return True
    
        return False
    
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = len([
            transacao for transacao in self.historico.transacoes
            if transacao.__class__.__name__.lower() == "saque"
        ])

        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False

        if valor > self.limite:
            print("O valor do saque excede o limite.")
            return False

        if numero_saques >= self.limite_saques:
            print("Numero maximo de saques excedido.")
            return False

        return super().sacar(valor)
    
    
class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass


class deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self.transacoes = []
        
    def adicionar_transacao(self,transacao):
        self.transacoes.append(transacao)


