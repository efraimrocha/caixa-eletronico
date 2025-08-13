class ClienteSchema:
    def __init__(self, nome: str, cpf: str, data_nascimento: str, endereco: str):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco

    def validar(self):
        if not self.cpf.isdigit() or len(self.cpf) != 11:
            raise ValueError("CPF inválido")
        # Adicione outras validações necessárias

class ContaSchema:
    def __init__(self, agencia: str, numero: int, cliente_cpf: str):
        self.agencia = agencia
        self.numero = numero
        self.cliente_cpf = cliente_cpf

class TransacaoSchema:
    def __init__(self, tipo: str, valor: float, conta_id: int):
        self.tipo = tipo
        self.valor = valor
        self.conta_id = conta_id