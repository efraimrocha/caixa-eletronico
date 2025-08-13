from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from banco.core.transacao import Transacao
from banco.utils.log import Logger

@dataclass
class Conta:
    agencia: str
    numero: int
    cliente: 'Cliente'
    saldo: float = 0.0
    extrato: List[str] = field(default_factory=list)
    data_abertura: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    _limite_saques: int = 3
    _limite: float = 500.0
    id: int = None
    logger: Logger = Logger()

    def __post_init__(self):
        self.logger.registrar("CONTA_CRIADA", {
            "Agência": self.agencia,
            "Número": self.numero,
            "Cliente": str(self.cliente)
        })

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: +R$ {valor:.2f}")
            self.logger.registrar("DEPÓSITO", {
                "Conta": f"{self.agencia}-{self.numero}",
                "Valor": f"R$ {valor:.2f}",
                "Saldo": f"R$ {self.saldo:.2f}"
            })
            return True
        return False

    def sacar(self, valor: float) -> bool:
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self._limite
        excedeu_saques = len([t for t in self.extrato if "Saque" in t]) >= self._limite_saques

        if excedeu_saldo:
            raise ValueError("Saldo insuficiente")
        elif excedeu_limite:
            raise ValueError("Valor excede o limite por saque")
        elif excedeu_saques:
            raise ValueError("Limite diário de saques atingido")
        elif valor > 0:
            self.saldo -= valor
            self.extrato.append(f"Saque: -R$ {valor:.2f}")
            self.logger.registrar("SAQUE", {
                "Conta": f"{self.agencia}-{self.numero}",
                "Valor": f"R$ {valor:.2f}",
                "Saldo": f"R$ {self.saldo:.2f}"
            })
            return True
        raise ValueError("Valor inválido")

    def get_extrato(self) -> str:
        self.logger.registrar("EXTRATO_SOLICITADO", {
            "Conta": f"{self.agencia}-{self.numero}"
        })
        header = f"""
        =============== EXTRATO ===============
        Agência: {self.agencia}
        Conta: {self.numero}
        Cliente: {self.cliente}
        Saldo: R$ {self.saldo:.2f}
        =======================================
        """
        movimentacoes = "\n".join(self.extrato) if self.extrato else "Nenhuma movimentação"
        return f"{header}\n{movimentacoes}"