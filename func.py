import textwrap
from datetime import datetime

def data_atual():
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y : %H:%M:%S")
    return data_e_hora_em_texto

def menu():
    menu = """
    =============== Banco Universal ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    ==============================================
    Informe a opção desejada.
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\nOperação realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    print("\n=============== Banco Universal ===============\n")
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número de saques excedido.")
    elif valor > 0:
        saldo -= valor
        numero_saques += 1          
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
        print("\n=============== Banco Universal ===============\n")
    return saldo, extrato
            
def exibir_extrato(saldo, /, *, extrato):
    print("\n=============== EXTRATO ===============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")

def cirar_usuario(usuarios):
    
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    # Verifica pelo CPF se o usuário já existe cadastrado
    if usuario:
        print("Usuário já existente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaa): ")
    endereco = input("Irforme o endereço (logradouro, nro - bairro - cidade/sigle estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco })
    
    print("\tUsuário criado com sucesso!")
    
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        data_atual = data_atual()
        sucesso = f"""\
        \t========== Conta criada com sucesso! =========
        \t==============================================
        \t    Agência:\t{agencia}
        \t    Número da conta:\t{numero_conta}
        \t    Data de abertura:\t{data_atual}
        """
        print("="*46)
        print("\tConta criada com sucesso! ")
        print(f"\t{data_atual}")
        print("="*46)
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("="*46)
    print("\nUsuário não encontrado, operação encerrada!")
    print(f"\t{data_atual}")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            Nro. Conta:\t{conta["numero_conta"]}
            Titular:\t{conta["usuario"]["nome"]}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))