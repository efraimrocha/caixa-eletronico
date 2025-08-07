import textwrap
from datetime import datetime
from functools import wraps

# Variável global para armazenar o histórico de transações
historico_transacoes = []

# Decorador para log de transações
def log_transacao(func):
    @wraps(func)
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historico_transacoes.append({
            'data_hora': data_hora,
            'transacao': func.__name__.upper(),
            'args': args,
            'kwargs': kwargs,
            'resultado': resultado
        })
        print(f"\n[{data_hora}] Transação: {func.__name__.upper()} realizada")
        return resultado
    return envelope

def data_atual():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#@log_transacao
def menu():
    menu_texto = """
    =============== Banco Universal ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [rl]\tRelatórios
    [q]\tSair
    ==============================================
    Informe a opção desejada.
    => """
    return input(textwrap.dedent(menu_texto))

@log_transacao
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\nOperação realizada com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    return saldo, extrato

@log_transacao
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\nOperação realizada com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

@log_transacao
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

@log_transacao
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\nUsuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

@log_transacao
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "data_criacao": data_atual()
        }

    print("\nUsuário não encontrado, operação encerrada!")
    return None

@log_transacao
def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada!")
        return

    print("\n================ CONTAS ================")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Criada em:\t{conta['data_criacao']}
        """
        print(textwrap.dedent(linha))
        print("==========================================")

@log_transacao
def mostrar_relatorios(usuarios, contas):
    print("\nSelecione o tipo de relatório:")
    print("1 - Transações")
    print("2 - Contas")
    print("3 - Usuários")
    print("4 - Completo")
    opcao = input("=> ")

    if opcao == "1":
        print("\n=== HISTÓRICO DE TRANSAÇÕES ===")
        for transacao in historico_transacoes:
            print(f"\nData: {transacao['data_hora']}")
            print(f"Tipo: {transacao['transacao']}")
            if transacao['transacao'] == 'DEPOSITAR':
                print(f"Valor: R$ {transacao['args'][1]:.2f}")
            elif transacao['transacao'] == 'SACAR':
                print(f"Valor: R$ {transacao['kwargs']['valor']:.2f}")
    elif opcao == "2":
        listar_contas(contas)
    elif opcao == "3":
        if not usuarios:
            print("\nNenhum usuário cadastrado!")
            return
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for usuario in usuarios:
            print(f"\nNome: {usuario['nome']}")
            print(f"CPF: {usuario['cpf']}")
    elif opcao == "4":
        print("\n=== RELATÓRIO COMPLETO ===")
        print("\n[TRANSAÇÕES]")
        mostrar_relatorios(usuarios, contas)
        print("\n[CONTAS]")
        listar_contas(contas)
        print("\n[USUÁRIOS]")
        mostrar_relatorios(usuarios, contas)
    else:
        print("\nOpção inválida!")