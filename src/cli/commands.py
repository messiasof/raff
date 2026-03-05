import argparse
from src.config import *
from pathlib import Path
###################################################################################################################
def run():
    from src.main import main
    main()

def test():
    print("Raff iniciando")
    DATA_DIR.mkdir(exist_ok=True)
    

#def stop():
#    print("Parando Raff...") # Adicionar lógica

###################################################################################################################

def mainCLI():
    parser = argparse.ArgumentParser(prog="raff")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

# -----------------------------------------------------------------------------------------------------------------
    # PARSER | start
    subparsers.add_parser("start", help="Inicia o Raff")
    subparsers.add_parser("test", help="Testa o Raff")

# -----------------------------------------------------------------------------------------------------------------
    args = parser.parse_args()

    if args.command == "start":
        run()
    elif args.command == "test":
        test()
    #elif args.command == "stop":
    #    stop()
    else:
        parser.print_help()

if __name__ == "__main__":
    mainCLI()