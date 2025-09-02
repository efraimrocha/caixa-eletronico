import json
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, arquivo_log: str = 'sistema.log'):
        self.arquivo_log = arquivo_log
        self._criar_diretorio_log()

    def _criar_diretorio_log(self):
        """Cria o diretório de logs se não existir"""
        Path(self.arquivo_log).parent.mkdir(parents=True, exist_ok=True)

    def registrar(self, evento: str, dados: dict):
        """Registra um evento no log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'evento': evento,
            'dados': dados
        }
        
        try:
            with open(self.arquivo_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Erro ao escrever no log: {e}")

    def ler_logs(self) -> list:
        """Lê todos os logs do arquivo"""
        logs = []
        try:
            if Path(self.arquivo_log).exists():
                with open(self.arquivo_log, 'r', encoding='utf-8') as f:
                    for linha in f:
                        logs.append(json.loads(linha.strip()))
        except Exception as e:
            print(f"Erro ao ler logs: {e}")
        
        return logs
