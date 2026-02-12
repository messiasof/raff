import argparse
import src.main
###################################################################################################################
def run():
    print("Raff iniciando...")
    src.main.main()

#def stop():
#    print("Parando Raff...") # Adicionar lógica

###################################################################################################################

def main():
    parser = argparse.ArgumentParser(prog="raff")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

# -----------------------------------------------------------------------------------------------------------------
    # PARSER | start
    subparsers.add_parser("start", help="Inicia o Raff")
# -----------------------------------------------------------------------------------------------------------------
    args = parser.parse_args()

    if args.command == "start":
        run()
    #elif args.command == "stop":
    #    stop()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()