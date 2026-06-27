from pathlib import Path
from datetime import datetime
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO = BASE_DIR / "main.py"

PASTA_BACKUP = BASE_DIR / "backups"
PASTA_BACKUP.mkdir(exist_ok=True)

nome = f"main_{datetime.now():%Y%m%d_%H%M%S}.py"

destino = PASTA_BACKUP / nome

shutil.copy2(ARQUIVO, destino)

print("=" * 50)
print("BACKUP REALIZADO COM SUCESSO")
print("=" * 50)
print(destino)