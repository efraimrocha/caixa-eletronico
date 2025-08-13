import logging
from datetime import datetime
from pathlib import Path

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializado = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inicializado'):
            self._inicializado = False
        if not self._inicializado:
            self.log_dir = Path(__file__).parent.parent / "logs"
            self.log_dir.mkdir(exist_ok=True)
            
            logging.basicConfig(
                filename=self.log_dir / "banco.log",
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
                encoding='utf-8'
            )
            self.logger = logging.getLogger("banco")
            self._inicializado = True

    def registrar(self, operacao: str, detalhes: dict):
        mensagem = f"{operacao.upper()}"
        for chave, valor in detalhes.items():
            mensagem += f" | {chave}: {valor}"
        
        self.logger.info(mensagem)
        self._log_console(mensagem)

    def _log_console(self, mensagem: str):
        print(f"[SISTEMA] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {mensagem}")