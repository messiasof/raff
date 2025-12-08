import subprocess
from pathlib import Path
from configplaceholder._config import baseDir, configDir

varPath = f"{baseDir}/{configDir}/var.txt"
lastvaluepath = f"{baseDir}/{configDir}/.lastvalue"
lastcheckpath = f"{baseDir}/{configDir}/.lastcheck"

def editVarFile(value):
    with open(varPath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())

def editLastValueFile(value):
      with open(lastvaluepath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())

def editLastCheckFile(value):
      with open(lastcheckpath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())


print(varPath)
print(lastcheckpath)
print(lastvaluepath)