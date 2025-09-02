from banco.core.banco import Banco
from banco.core.cliente import Cliente
from datetime import datetime
import re

def limpar_tela():
    """Limpa a tela do terminal"""
    print("\n" * 50)

def formatar_cpf(cpf: str) -> str:
    """Formata o CPF para exibição"""
    cpf_numeros = re.sub(r'\D', '', cpf)
    if len(cpf_numeros) == 11:
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    return cpf

def menu_principal():
    """Exibe o menu principal"""
    print("=" * 50)
    print("SISTEMA BANCÁRIO")
    print("=" * 50)
    print("1. Cadastrar Cliente")
    print("2. Criar Conta")
    print("3. Depositar")
    print("4. Sacar")
    print("5. Transferir")
    print("6. Consultar Saldo")
    print("7. Listar Contas de Cliente")
    print("8. Sair")
    print("=" * 50)

def main():
    banco = Banco()
    
    while True:
        try:
            limpar_tela()
            menu_principal()
            
            opcao = input("Opção: ").strip()
            
            if opcao == "1":
                cadastrar_cliente(banco)
            elif opcao == "2":
                criar_conta(banco)
            elif opcao == "3":
                depositar(banco)
            elif opcao == "4":
                sacar(banco)
            elif opcao == "5":
                transferir(banco)
            elif opcao == "6":
                consultar_saldo(banco)
            elif opcao == "7":
                listar_contas_cliente(banco)
            elif opcao == "8":
                print("Saindo do sistema...")
                break
            else:
                input("Opção inválida. Pressione Enter para continuar...")
                
        except Exception as e:
            input(f"❌ Erro: {e}. Pressione Enter para continuar...")

def cadastrar_cliente(banco: Banco):
    """Cadastra um novo cliente"""
    print("\n--- CADASTRAR CLIENTE ---")
    
    cpf = input("CPF: ").strip()
    nome = input("Nome: ").strip()
    data_nascimento = input("Data de Nascimento (YYYY-MM-DD): ").strip()
    
    try:
        data_nasc = datetime.strptime(data_nascimento, "%Y-%m-%d")
        cliente = Cliente(cpf=cpf, nome=nome, data_nascimento=data_nasc)
        
        if banco.cadastrar_cliente(cliente):
            print("✅ Cliente cadastrado com sucesso!")
        else:
            print("❌ Erro ao cadastrar cliente.")
            
    except ValueError as e:
        print(f"❌ Erro: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    input("Pressione Enter para continuar...")

def criar_conta(banco: Banco):
    """Cria uma nova conta"""
    print("\n--- CRIAR CONTA ---")
    
    cpf = input("CPF do Cliente: ").strip()
    agencia = "0001"  # Agência fixa para simplificação
    
    try:
        conta = banco.criar_conta(agencia, cpf)
        print(f"✅ Conta criada com sucesso!")
        print(f"   Agência: {conta.agencia}")
        print(f"   Número: {conta.numero}")
        print(f"   Titular: {conta.cliente.nome}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("Pressione Enter para continuar...")

def depositar(banco: Banco):
    """Realiza um depósito"""
    print("\n--- DEPOSITAR ---")
    
    agencia = input("Agência: ").strip()
    numero = int(input("Número da Conta: ").strip())
    valor = float(input("Valor: ").strip())
    
    try:
        conta = banco.buscar_conta(agencia, numero)
        if conta:
            conta.depositar(valor)
            banco.db.atualizar_saldo(agencia, numero, conta.saldo)
            print(f"✅ Depósito realizado com sucesso!")
            print(f"   Novo saldo: R$ {conta.saldo:.2f}")
        else:
            print("❌ Conta não encontrada.")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("Pressione Enter para continuar...")

def sacar(banco: Banco):
    """Realiza um saque"""
    print("\n--- SACAR ---")
    
    agencia = input("Agência: ").strip()
    numero = int(input("Número da Conta: ").strip())
    valor = float(input("Valor: ").strip())
    
    try:
        conta = banco.buscar_conta(agencia, numero)
        if conta:
            conta.sacar(valor)
            banco.db.atualizar_saldo(agencia, numero, conta.saldo)
            print(f"✅ Saque realizado com sucesso!")
            print(f"   Novo saldo: R$ {conta.saldo:.2f}")
        else:
            print("❌ Conta não encontrada.")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("Pressione Enter para continuar...")

def transferir(banco: Banco):
    """Realiza uma transferência"""
    print("\n--- TRANSFERIR ---")
    
    agencia_origem = input("Agência Origem: ").strip()
    numero_origem = int(input("Número Conta Origem: ").strip())
    agencia_destino = input("Agência Destino: ").strip()
    numero_destino = int(input("Número Conta Destino: ").strip())
    valor = float(input("Valor: ").strip())
    
    try:
        conta_origem = banco.buscar_conta(agencia_origem, numero_origem)
        conta_destino = banco.buscar_conta(agencia_destino, numero_destino)
        
        if conta_origem and conta_destino:
            conta_origem.transferir(valor, conta_destino)
            banco.db.atualizar_saldo(agencia_origem, numero_origem, conta_origem.saldo)
            banco.db.atualizar_saldo(agencia_destino, numero_destino, conta_destino.saldo)
            print(f"✅ Transferência realizada com sucesso!")
        else:
            print("❌ Conta(s) não encontrada(s).")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("Pressione Enter para continuar...")

def consultar_saldo(banco: Banco):
    """Consulta o saldo de uma conta"""
    print("\n--- CONSULTAR SALDO ---")
    
    agencia = input("Agência: ").strip()
    numero = int(input("Número da Conta: ").strip())
    
    try:
        conta = banco.buscar_conta(agencia, numero)
        if conta:
            print(f"💰 Saldo: R$ {conta.saldo:.2f}")
            print(f"   Titular: {conta.cliente.nome}")
        else:
            print("❌ Conta não encontrada.")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("Pressione Enter para continuar...")

def listar_contas_cliente(banco: Banco):
    """Lista todas as contas de um cliente"""
    print("\n--- LISTAR CONTAS DO CLIENTE ---")
    
    cpf = input("CPF do Cliente: ").strip()
    
    try:
        contas = banco.listar_contas_cliente(cpf)
        if contas:
            print(f"📋 Contas do cliente:")
            for conta in contas:
                print(f"   Agência: {conta.agencia} | Número: {conta.numero} | Saldo: R$ {conta.saldo:.2f}")
        else:
            print("❌ Nenhuma conta encontrada para este cliente.")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
