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
    
    # PARSER | warn
    warn_parser = subparsers.add_parser("warn", help="Exibe um aviso customizado")
    warn_parser.add_argument("message", nargs="?", default="Aviso do R.A.F.F", help="Mensagem do aviso")

# -----------------------------------------------------------------------------------------------------------------
    args = parser.parse_args()

    if args.command == "start":
        run()
    elif args.command == "test":
        test()
    elif args.command == "warn":
        from src.warn import show_warning
        show_warning(args.message)
    #elif args.command == "stop":
    #    stop()
    else:
        parser.print_help()

if __name__ == "__main__":
    mainCLI()