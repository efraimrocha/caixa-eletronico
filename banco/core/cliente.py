from dataclasses import dataclass
from banco.utils.log import Logger

@dataclass
class Cliente:
    nome: str
    cpf: str
    data_nascimento: str
    endereco: str
    logger: Logger = Logger()

    def __post_init__(self):
        self.logger.registrar("CLIENTE_CRIADO", {
            "Nome": self.nome,
            "CPF": self.cpf[:3] + ".***.***-**"
        })

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf[:3]}.XXX.XXX-XX)"