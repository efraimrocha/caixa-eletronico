from func import *

def main():
    # Constantes do sistema
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    # Variáveis de estado
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        try:
            opcao = menu()

            # Operação de Depósito
            if opcao == "d":
                try:
                    valor = float(input("\nInforme o valor do depósito: "))
                    saldo, extrato = depositar(saldo, valor, extrato)
                except ValueError:
                    print("\nErro: Valor inválido. Digite um número.")

            # Operação de Saque
            elif opcao == "s":
                try:
                    valor = float(input("\nInforme o valor do saque: "))
                    saldo, extrato, numero_saques = sacar(
                        saldo=saldo,
                        valor=valor,
                        extrato=extrato,
                        limite=limite,
                        numero_saques=numero_saques,
                        limite_saques=LIMITE_SAQUES,
                    )
                except ValueError:
                    print("\nErro: Valor inválido. Digite um número.")

            # Visualização de Extrato
            elif opcao == "e":
                exibir_extrato(saldo, extrato=extrato)

            # Cadastro de Novo Usuário
            elif opcao == "nu":
                criar_usuario(usuarios)

            # Criação de Nova Conta
            elif opcao == "nc":
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                if conta:
                    contas.append(conta)
                    numero_conta += 1

            # Listagem de Contas
            elif opcao == "lc":
                listar_contas(contas)

            # Relatórios
            elif opcao == "rl":
                mostrar_relatorios(usuarios, contas)

            # Saída do Sistema
            elif opcao == "q":
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                mensagem_saida = f"""
                ==============================================
                         {data_hora}
                === OBRIGADO POR USAR NOSSO SISTEMA! ===
                """
                print(textwrap.dedent(mensagem_saida))
                break

            # Opção inválida
            else:
                print("\nOperação inválida! Por favor selecione uma opção válida.")

        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
            print("Por favor, tente novamente.")

if __name__ == "__main__":
    main()