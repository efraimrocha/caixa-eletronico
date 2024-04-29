# caixa-eletronico
Repositório para desafio de código do bootcamp Python AI backend VIVO.

# Sistema Bancário Simples

Este é um programa simples de simulação de operações bancárias. O programa permite que o usuário realize depósitos, saques, veja o extrato e saia do programa.

## Funcionalidades

O programa possui as seguintes funcionalidades:

1. **Depositar [d]**: Esta opção permite ao usuário fazer um depósito. O usuário deve informar o valor do depósito. Se o valor for maior que 0, o valor é adicionado ao saldo e registrado no extrato.

2. **Sacar [s]**: Esta opção permite ao usuário fazer um saque. O usuário deve informar o valor do saque. Existem algumas restrições para esta operação:
    - O valor do saque não pode exceder o saldo disponível.
    - O valor do saque não pode exceder o limite de saque definido (R$ 500).
    - O número de saques não pode exceder o limite de saques definido (3 saques).
    Se o valor do saque for maior que 0 e nenhuma das restrições for violada, o valor é subtraído do saldo e registrado no extrato.

3. **Extrato [e]**: Esta opção permite ao usuário ver o extrato das operações realizadas. O extrato mostra todas as operações de depósito e saque realizadas, bem como o saldo atual.

4. **Sair [q]**: Esta opção permite ao usuário sair do programa.

## Como usar

Para usar o programa, basta executá-lo e seguir as instruções exibidas no console. O usuário deve escolher uma das opções do menu (d, s, e, q) e seguir as instruções correspondentes.

## Notas

Este programa é uma simulação simples e não deve ser usado para operações bancárias reais.

