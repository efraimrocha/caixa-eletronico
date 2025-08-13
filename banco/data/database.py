import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from ..core.cliente import Cliente
from ..core.conta import Conta

DB_PATH = Path(__file__).parent / "banco.db"

class BancoDeDados:
    def __init__(self):
        self._criar_tabelas()
        self.conn = self._conectar()

    def _conectar(self):
        """Estabelece conexão com o banco de dados"""
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")  # Ativa chaves estrangeiras
        return conn

    def _criar_tabelas(self):
        """Cria as tabelas se não existirem"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela de Clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    cpf TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    endereco TEXT NOT NULL
                )
            """)
            
            # Tabela de Contas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agencia TEXT NOT NULL,
                    numero INTEGER NOT NULL,
                    saldo REAL NOT NULL DEFAULT 0,
                    cliente_cpf TEXT NOT NULL,
                    data_abertura TEXT NOT NULL,
                    FOREIGN KEY (cliente_cpf) REFERENCES clientes(cpf) ON DELETE CASCADE,
                    UNIQUE(agencia, numero)
                )
            """)
            
            # Tabela de Transações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conta_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    valor REAL NOT NULL,
                    data TEXT NOT NULL,
                    FOREIGN KEY (conta_id) REFERENCES contas(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def salvar_cliente(self, cliente: Cliente) -> bool:
        """Salva um cliente no banco de dados"""
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO clientes VALUES (?, ?, ?, ?)",
                    (cliente.cpf, cliente.nome, cliente.data_nascimento, cliente.endereco)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def buscar_cliente(self, cpf: str) -> Optional[Cliente]:
        """Busca um cliente pelo CPF"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        return Cliente(*resultado) if resultado else None

    def salvar_conta(self, conta: Conta) -> bool:
        """Salva uma conta no banco de dados"""
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    """INSERT INTO contas 
                    (agencia, numero, cliente_cpf, data_abertura) 
                    VALUES (?, ?, ?, ?)""",
                    (conta.agencia, conta.numero, conta.cliente.cpf, conta.data_abertura)
                )
                conta.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro ao salvar conta: {e}")
            return False

    def buscar_conta(self, agencia: str, numero: int) -> Optional[Conta]:
        """Busca uma conta por agência e número"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.id, c.agencia, c.numero, c.saldo, c.data_abertura,
                   cl.cpf, cl.nome, cl.data_nascimento, cl.endereco
            FROM contas c
            JOIN clientes cl ON c.cliente_cpf = cl.cpf
            WHERE c.agencia = ? AND c.numero = ?
        """, (agencia, numero))
        
        resultado = cursor.fetchone()
        if resultado:
            conta = Conta(
                agencia=resultado[1],
                numero=resultado[2],
                cliente=Cliente(
                    nome=resultado[6],
                    cpf=resultado[5],
                    data_nascimento=resultado[7],
                    endereco=resultado[8]
                ),
                saldo=resultado[3],
                data_abertura=resultado[4]
            )
            conta.id = resultado[0]
            return conta
        return None

    def atualizar_saldo(self, conta_id: int, novo_saldo: float) -> bool:
        """Atualiza o saldo de uma conta"""
        try:
            with self.conn:
                self.conn.execute(
                    "UPDATE contas SET saldo = ? WHERE id = ?",
                    (novo_saldo, conta_id)
                )
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar saldo: {e}")
            return False

    def registrar_transacao(self, conta_id: int, tipo: str, valor: float) -> bool:
        """Registra uma transação no banco de dados"""
        try:
            with self.conn:
                self.conn.execute(
                    """INSERT INTO transacoes 
                    (conta_id, tipo, valor, data) 
                    VALUES (?, ?, ?, datetime('now'))""",
                    (conta_id, tipo, valor)
                )
            return True
        except sqlite3.Error as e:
            print(f"Erro ao registrar transação: {e}")
            return False

    def __del__(self):
        """Fecha a conexão quando o objeto é destruído"""
        if hasattr(self, 'conn'):
            self.conn.close()