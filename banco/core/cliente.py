from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cliente:
    cpf: str
    nome: str
    data_nascimento: datetime

    def __post_init__(self):
        """Validações após inicialização"""
        if not self.validar_cpf():
            raise ValueError("CPF inválido")
        
        if not self.nome or len(self.nome.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        
        if not isinstance(self.data_nascimento, datetime):
            raise ValueError("Data de nascimento deve ser um objeto datetime")

    def validar_cpf(self) -> bool:
        """Validação básica de CPF"""
        cpf = ''.join(filter(str.isdigit, self.cpf))
        return len(cpf) == 11 and cpf != cpf[0] * 11
