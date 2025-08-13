from datetime import datetime

def formatar_data(data: str) -> str:
    """Formata data para dd/mm/aaaa"""
    try:
        return datetime.strptime(data, "%d-%m-%Y").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Formato de data inválido. Use dd-mm-aaaa")

def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF tem 11 dígitos numéricos"""
    return cpf.isdigit() and len(cpf) == 11