# 🏦 Caixa Eletrônico - Sistema Bancário em Python

Sistema bancário completo para gerenciamento de clientes, contas e operações financeiras, desenvolvido em Python.

---

## 📋 Funcionalidades

- **Gestão de Clientes**
  - Cadastro com validação de CPF
  - Armazenamento seguro de dados pessoais
  - Verificação de duplicidade

- **Gestão de Contas**
  - Criação de contas correntes
  - Números de conta sequenciais por agência
  - Múltiplas contas por cliente
  - Consulta de contas

- **Operações Financeiras**
  - Depósitos
  - Saques com validação de saldo
  - Transferências entre contas
  - Consulta de saldo

---

## 🛠️ Tecnologias

- Python 3.8+
- SQLite3 (banco de dados)
- Dataclasses
- JSON (logging estruturado)

---

## 📦 Estrutura do Projeto

```
caixa-eletronico/
├── banco/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── banco.py          # Classe principal
│   │   ├── cliente.py        # Entidade Cliente
│   │   └── conta.py          # Entidade Conta
│   ├── data/
│   │   ├── __init__.py
│   │   └── database.py       # Banco de dados
│   └── utils/
│       ├── __init__.py
│       └── log.py            # Logging
├── main.py                   # CLI
├── banco.db                  # Banco de dados gerado
├── sistema.log               # Logs gerados
└── README.md
```

---

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/efraimrocha/caixa-eletronico.git
   cd caixa-eletronico
   ```
2. Instale dependências (se necessário):
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o sistema:
   ```bash
   python main.py
   ```

---

## 🚀 Exemplos de Uso

**Cadastrar cliente**
```
Opção: 1
CPF: 12345678900
Nome: João Silva
Data de Nascimento: 1990-01-15
```

**Criar conta**
```
Opção: 2
CPF do Cliente: 12345678900
```

**Realizar depósito**
```
Opção: 3
Agência: 0001
Número da Conta: 1
Valor: 1000.00
```

---

## 🗃️ Estrutura de Dados

**Clientes**
| Campo           | Tipo      | Descrição                  |
|-----------------|-----------|----------------------------|
| cpf             | TEXT (PK) | CPF do cliente             |
| nome            | TEXT      | Nome completo              |
| data_nascimento | TEXT      | Data de nascimento (ISO)   |

**Contas**
| Campo         | Tipo        | Descrição                  |
|---------------|-------------|----------------------------|
| agencia       | TEXT (PK)   | Número da agência          |
| numero        | INTEGER(PK) | Número da conta            |
| cliente_cpf   | TEXT (FK)   | CPF do titular             |
| saldo         | REAL        | Saldo atual                |
| data_abertura | TEXT        | Data de abertura (ISO)     |

---

## 🔒 Segurança

- CPFs mascarados nos logs
- Validação de todas as operações
- Transações atômicas
- Auditoria completa via logs

---

## 📊 Logs

Logs detalhados em `sistema.log` no formato JSON:

```json
{
  "timestamp": "2024-01-15T10:30:00.000000",
  "evento": "CONTA_CRIADA",
  "dados": {
    "agencia": "0001",
    "numero": 1,
    "cliente": "João Silva",
    "cpf": "123.***.***-**"
  }
}
```

---

## 🧪 Testes e Qualidade

- Validações robustas de entrada
- Tratamento completo de erros
- Consistência de dados garantida
- Prevenção de condições de corrida

---

## 🐛 Solução de Problemas

- **Cliente já cadastrado:** CPF já existe
- **Conta não encontrada:** Verifique agência e número
- **Saldo insuficiente:** Fundos insuficientes

Consulte `sistema.log` para detalhes técnicos.

---

## 📈 Próximas Melhorias

- Interface web
- API RESTful
- Autenticação de usuários
- Extratos detalhados
- Investimentos e poupança
- Pagamento de contas
- Integração com Pix

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças
4. Push para sua branch
5. Abra um Pull Request

---

## 📄 Licença

Projeto sob licença MIT. Veja o arquivo LICENSE.

---

## 👨‍💻 Autor

**Efraim Rocha**  
GitHub: [@efraimrocha](https://github.com/efraimrocha)  
Email: efraimrocha86@gmail.com

---

## 🙏 Agradecimentos

- Digital Inovation One
- Suzano
- Comunidade Python
- Contribuidores e testadores

---

> ⚠️ **Disclaimer:** Sistema educacional. Não utilize para operações bancárias reais.
