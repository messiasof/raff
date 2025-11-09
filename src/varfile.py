import subprocess
from pathlib import Path
from _config import baseDir

varPath = baseDir/"var.txt"
lastvaluepath = baseDir/".lastvalue"
lastcheckpath = baseDir/".lastcheck"

def editVarFile(value):
    with open(varPath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())

def editLastValueFile(value):
      with open(lastvaluepath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())

def editLastCheckFile(value):
      with open(lastcheckpath, "w", encoding="utf-8") as f:
            f.write(str(value).strip())