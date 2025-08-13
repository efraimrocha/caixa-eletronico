from abc import ABC, abstractmethod
from banco.utils.log import Logger

class Transacao(ABC):
    def __init__(self):
        self.logger = Logger()

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            return "Depósito realizado com sucesso"
        return "Falha no depósito"

class Saque(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        try:
            if conta.sacar(self.valor):
                return "Saque realizado com sucesso"
        except ValueError as e:
            self.logger.registrar("ERRO_SAQUE", {
                "Conta": f"{conta.agencia}-{conta.numero}",
                "Erro": str(e)
            })
            raise