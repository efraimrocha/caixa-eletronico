import sqlite3
from typing import Optional, List
from datetime import datetime
from ..core.cliente import Cliente
from ..core.conta import Conta

class BancoDeDados:
    def __init__(self, nome_banco: str = 'banco.db'):
        self.nome_banco = nome_banco
        self.conn = sqlite3.connect(nome_banco, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._criar_tabelas()

    def _criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        cursor = self.conn.cursor()
        
        # Tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL
            )
        ''')
        
        # Tabela de contas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                agencia TEXT NOT NULL,
                numero INTEGER NOT NULL,
                cliente_cpf TEXT NOT NULL,
                saldo REAL DEFAULT 0,
                data_abertura TEXT NOT NULL,
                PRIMARY KEY (agencia, numero),
                FOREIGN KEY (cliente_cpf) REFERENCES clientes(cpf) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()

    def salvar_cliente(self, cliente: Cliente) -> bool:
        """Salva um cliente no banco de dados"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO clientes (cpf, nome, data_nascimento)
                VALUES (?, ?, ?)
            ''', (cliente.cpf, cliente.nome, cliente.data_nascimento.isoformat()))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao salvar cliente: {e}")

    def buscar_cliente(self, cpf: str) -> Optional[Cliente]:
        """Busca um cliente pelo CPF"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT cpf, nome, data_nascimento FROM clientes WHERE cpf = ?
            ''', (cpf,))
            
            row = cursor.fetchone()
            if row:
                return Cliente(
                    cpf=row['cpf'],
                    nome=row['nome'],
                    data_nascimento=datetime.fromisoformat(row['data_nascimento'])
                )
            return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao buscar cliente: {e}")

    def salvar_conta(self, conta: Conta) -> bool:
        """Salva uma conta no banco de dados"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO contas (agencia, numero, cliente_cpf, saldo, data_abertura)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                conta.agencia,
                conta.numero,
                conta.cliente.cpf,
                conta.saldo,
                conta.data_abertura.isoformat()
            ))
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise ValueError("Conta já existe ou cliente não encontrado")
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao salvar conta: {e}")

    def buscar_conta(self, agencia: str, numero: int) -> Optional[Conta]:
        """Busca uma conta pela agência e número"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT c.agencia, c.numero, c.saldo, c.data_abertura,
                       cl.cpf, cl.nome, cl.data_nascimento
                FROM contas c
                JOIN clientes cl ON c.cliente_cpf = cl.cpf
                WHERE c.agencia = ? AND c.numero = ?
            ''', (agencia, numero))
            
            row = cursor.fetchone()
            if row:
                cliente = Cliente(
                    cpf=row['cpf'],
                    nome=row['nome'],
                    data_nascimento=datetime.fromisoformat(row['data_nascimento'])
                )
                
                return Conta(
                    agencia=row['agencia'],
                    numero=row['numero'],
                    cliente=cliente,
                    saldo=row['saldo'],
                    data_abertura=datetime.fromisoformat(row['data_abertura'])
                )
            return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao buscar conta: {e}")

    def obter_ultimo_numero_conta(self, agencia: str) -> Optional[int]:
        """Obtém o último número de conta usado para uma agência"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT MAX(numero) FROM contas WHERE agencia = ?
            ''', (agencia,))
            
            resultado = cursor.fetchone()
            return resultado[0] if resultado and resultado[0] is not None else None
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao obter último número: {e}")

    def buscar_contas_cliente(self, cliente_cpf: str) -> List[Conta]:
        """Busca todas as contas de um cliente"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT c.agencia, c.numero, c.saldo, c.data_abertura,
                       cl.cpf, cl.nome, cl.data_nascimento
                FROM contas c
                JOIN clientes cl ON c.cliente_cpf = cl.cpf
                WHERE cl.cpf = ?
            ''', (cliente_cpf,))
            
            contas = []
            for row in cursor.fetchall():
                cliente = Cliente(
                    cpf=row['cpf'],
                    nome=row['nome'],
                    data_nascimento=datetime.fromisoformat(row['data_nascimento'])
                )
                
                conta = Conta(
                    agencia=row['agencia'],
                    numero=row['numero'],
                    cliente=cliente,
                    saldo=row['saldo'],
                    data_abertura=datetime.fromisoformat(row['data_abertura'])
                )
                contas.append(conta)
            
            return contas
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao buscar contas do cliente: {e}")

    def atualizar_saldo(self, agencia: str, numero: int, novo_saldo: float) -> bool:
        """Atualiza o saldo de uma conta"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE contas SET saldo = ? WHERE agencia = ? AND numero = ?
            ''', (novo_saldo, agencia, numero))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao atualizar saldo: {e}")

    def __del__(self):
        """Fecha a conexão com o banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()
