from func import *
        
def main():
        
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    nemero_conta = 1


    while True:
        opcao = menu()
        
        if opcao == "d":     
            valor = float(input("informe o valor do depósito: "))
            
            saldo, valor = depositar(saldo, valor, extrato)
            extrato += f"{valor}"
            
        elif opcao == "s":
            valor = float(input("informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
            
        elif opcao == "nu":
            cirar_usuario(usuarios)
            
        elif opcao == "nc":
            #nemero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, nemero_conta, usuarios)
            
            if conta:
                contas.append(conta)
                nemero_conta += 1
             
        elif opcao == "lc":
            listar_contas(contas)
           
        elif opcao == "q":
            data_hora = data_atual()
            saida = f"""\
            \t==============================================
            \t             {data_hora}
            \t==== OBRIGADO POR UTILIZAR NOSSO SISTEMA! ====
            """
            print(textwrap.dedent(saida))
            break
        else:
            print("Operação inválida, por favor selecione novamente a opção desejada. ")

main()