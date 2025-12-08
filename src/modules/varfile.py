import subprocess
from pathlib import Path
from src.configplaceholder._config import baseDir

varPath = f"{baseDir}\\var.txt"
lastvaluepath = f"{baseDir}\\.lastvalue"
lastcheckpath = f"{baseDir}\\.lastcheck"

def editVarFile(value):
    with open(varPath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())

def editLastValueFile(value):
      with open(lastvaluepath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())

def editLastCheckFile(value):
      with open(lastcheckpath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())
