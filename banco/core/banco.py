from banco.data.database import BancoDeDados
from banco.utils.log import Logger

class Banco:
    def __init__(self):
        self.db = BancoDeDados()
        self.logger = Logger()

    def cadastrar_cliente(self, cliente):
        try:
            if self.db.salvar_cliente(cliente):
                self.logger.registrar("CLIENTE_CADASTRADO", {
                    "Nome": cliente.nome,
                    "CPF": cliente.cpf[:3] + ".***.***-**"
                })
                return True
            return False
        except Exception as e:
            self.logger.registrar("ERRO_CADASTRO", {
                "Tipo": "Cliente",
                "Erro": str(e)
            })
            raise

    def criar_conta(self, agencia, cliente_cpf):
        try:
            conta = self.db.criar_conta(agencia, cliente_cpf)
            if conta:
                self.logger.registrar("CONTA_CRIADA", {
                    "Agência": conta.agencia,
                    "Número": conta.numero,
                    "Cliente": conta.cliente.nome
                })
                return conta
            return None
        except Exception as e:
            self.logger.registrar("ERRO_CONTA", {
                "Tipo": "Criação",
                "Erro": str(e)
            })
            raise

    def buscar_conta(self, agencia, numero):
        try:
            conta = self.db.buscar_conta(agencia, numero)
            if conta:
                self.logger.registrar("CONSULTA_CONTA", {
                    "Agência": agencia,
                    "Número": numero,
                    "Status": "Encontrada"
                })
                return conta
            raise ValueError("Conta não encontrada")
        except Exception as e:
            self.logger.registrar("ERRO_CONSULTA", {
                "Agência": agencia,
                "Número": numero,
                "Erro": str(e)
            })
            raise