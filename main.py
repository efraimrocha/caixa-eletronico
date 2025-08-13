from banco.core.banco import Banco
from banco.core.cliente import Cliente
from banco.core.transacao import Deposito, Saque
from banco.utils.log import Logger

def main():
    banco = Banco()
    logger = Logger()

    while True:
        print("\n=============== BANCO PROFISSIONAL ===============")
        print("1. Cadastrar Cliente")
        print("2. Criar Conta")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Extrato")
        print("6. Sair")
        opcao = input("Opção: ")

        try:
            if opcao == "1":
                nome = input("Nome: ").strip()
                cpf = input("CPF (apenas números): ").strip()
                data_nasc = input("Data Nasc. (dd/mm/aaaa): ").strip()
                endereco = input("Endereço: ").strip()
                
                if not nome or not cpf.isdigit() or len(cpf) != 11:
                    logger.registrar("ERRO_VALIDACAO", {"Tipo": "CPF inválido"})
                    print("❌ Dados inválidos!")
                    continue
                    
                cliente = Cliente(nome, cpf, data_nasc, endereco)
                if banco.cadastrar_cliente(cliente):
                    print("✅ Cliente cadastrado!")

            elif opcao == "2":
                cpf = input("CPF do Cliente: ").strip()
                if not cpf.isdigit() or len(cpf) != 11:
                    logger.registrar("ERRO_VALIDACAO", {"Tipo": "CPF inválido"})
                    print("❌ CPF inválido!")
                    continue
                    
                conta = banco.criar_conta("0001", cpf)
                if conta:
                    print(f"✅ Conta {conta.numero} criada!")

            elif opcao == "3":
                try:
                    agencia = input("Agência: ").strip()
                    numero = int(input("Número: "))
                    valor = float(input("Valor: "))
                    conta = banco.buscar_conta(agencia, numero)
                    print(Deposito(valor).registrar(conta))
                except ValueError as e:
                    print(f"❌ {e}")

            elif opcao == "4":
                try:
                    agencia = input("Agência: ").strip()
                    numero = int(input("Número: "))
                    valor = float(input("Valor: "))
                    conta = banco.buscar_conta(agencia, numero)
                    print(Saque(valor).registrar(conta))
                except ValueError as e:
                    print(f"❌ {e}")

            elif opcao == "5":
                try:
                    agencia = input("Agência: ").strip()
                    numero = int(input("Número: "))
                    conta = banco.buscar_conta(agencia, numero)
                    print(conta.get_extrato())
                except ValueError as e:
                    print(f"❌ {e}")

            elif opcao == "6":
                logger.registrar("SISTEMA", {"Status": "Encerrado"})
                print("Saindo...")
                break

            else:
                logger.registrar("ERRO_OPCAO", {"Opção": opcao})
                print("❌ Opção inválida!")

        except KeyboardInterrupt:
            logger.registrar("SISTEMA", {"Status": "Interrompido pelo usuário"})
            print("\nOperação cancelada pelo usuário")
            break
        except Exception as e:
            logger.registrar("ERRO_INESPERADO", {"Detalhes": str(e)})
            print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()