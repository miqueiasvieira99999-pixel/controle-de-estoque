from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
MAIN = BASE_DIR / "main.py"

print("=" * 60)
print("ERP Developer Tools")
print("=" * 60)

texto = MAIN.read_text(encoding="utf-8")

funcoes = re.findall(
    r"^def\s+([a-zA-Z0-9_]+)\s*\(",
    texto,
    re.MULTILINE,
)

print(f"\nFunções encontradas: {len(funcoes)}\n")

for i, nome in enumerate(funcoes, start=1):
    print(f"{i:02d} - {nome}")