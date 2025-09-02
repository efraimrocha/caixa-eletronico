from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .cliente import Cliente

@dataclass
class Conta:
    agencia: str
    numero: int
    cliente: Cliente
    saldo: float = 0.0
    data_abertura: Optional[datetime] = None

    def __post_init__(self):
        """Validações após inicialização"""
        if not self.agencia or len(self.agencia) != 4:
            raise ValueError("Agência deve ter 4 dígitos")
        
        if self.numero <= 0:
            raise ValueError("Número da conta deve ser positivo")
        
        if not isinstance(self.cliente, Cliente):
            raise ValueError("Cliente deve ser uma instância da classe Cliente")
        
        if self.saldo < 0:
            raise ValueError("Saldo não pode ser negativo")
        
        if self.data_abertura is None:
            self.data_abertura = datetime.now()

    def depositar(self, valor: float) -> bool:
        """Realiza um depósito na conta"""
        if valor <= 0:
            raise ValueError("Valor do depósito deve ser positivo")
        
        self.saldo += valor
        return True

    def sacar(self, valor: float) -> bool:
        """Realiza um saque na conta"""
        if valor <= 0:
            raise ValueError("Valor do saque deve ser positivo")
        
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente")
        
        self.saldo -= valor
        return True

    def transferir(self, valor: float, conta_destino: 'Conta') -> bool:
        """Realiza uma transferência para outra conta"""
        if valor <= 0:
            raise ValueError("Valor da transferência deve ser positivo")
        
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente")
        
        if not isinstance(conta_destino, Conta):
            raise ValueError("Conta destino inválida")
        
        self.saldo -= valor
        conta_destino.saldo += valor
        return True
