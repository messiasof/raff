import subprocess
from pathlib import Path
from _config import baseDir

varPath = baseDir/"var.txt" # Define o caminho para o var.txt

def editVarFile(value):
    with open(varPath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())