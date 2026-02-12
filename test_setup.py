"""
Script de teste para validar a instalação do R.A.F.F
Execute: python test_setup.py
"""

import sys
from pathlib import Path

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🔍 Testando imports...")
    
    try:
        from src import config
        print("  ✅ config.py")
    except Exception as e:
        print(f"  ❌ config.py - {e}")
        return False
    
    try:
        from src import storage
        print("  ✅ storage.py")
    except Exception as e:
        print(f"  ❌ storage.py - {e}")
        return False
    
    try:
        from src import network
        print("  ✅ network.py")
    except Exception as e:
        print(f"  ❌ network.py - {e}")
        return False
    
    try:
        from src import ai_engine
        print("  ✅ ai_engine.py")
    except Exception as e:
        print(f"  ❌ ai_engine.py - {e}")
        return False
    
    try:
        from src import ui
        print("  ✅ ui.py")
    except Exception as e:
        print(f"  ❌ ui.py - {e}")
        return False
    
    try:
        from src import app
        print("  ✅ app.py")
    except Exception as e:
        print(f"  ❌ app.py - {e}")
        return False
    
    return True


def test_env():
    """Testa se o .env existe e pode ser carregado."""
    print("\n🔍 Testando .env...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("  ❌ Arquivo .env não encontrado!")
        print("  ℹ️  Copie .env.example para .env e configure")
        return False
    
    print("  ✅ Arquivo .env encontrado")
    
    try:
        from src.config import (
            STUDENT_NAME, TEACHER_NAME, GEMINI_API_KEY,
            URL_QUESTIONS, URL_CHECK, CHECK_CHAR,
            AI_MODE, NETWORK_DEVICE_1, NETWORK_DEVICE_2
        )
        print(f"  ✅ Configurações carregadas:")
        print(f"     - Aluno: {STUDENT_NAME}")
        print(f"     - Responsável: {TEACHER_NAME}")
        print(f"     - Modo IA: {AI_MODE}")
        print(f"     - Adaptador 1: {NETWORK_DEVICE_1}")
        print(f"     - Adaptador 2: {NETWORK_DEVICE_2}")
        
        if not GEMINI_API_KEY or GEMINI_API_KEY == "sua_api_key_aqui" or GEMINI_API_KEY == "cole_sua_api_key_aqui":
            print("  ⚠️  GEMINI_API_KEY não configurada (necessária para modo IA)")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro ao carregar configurações: {e}")
        return False


def test_data_dir():
    """Testa se o diretório de dados pode ser criado."""
    print("\n🔍 Testando diretório de dados...")
    
    try:
        from src.config import DATA_DIR
        if DATA_DIR.exists():
            print(f"  ✅ Diretório existe: {DATA_DIR}")
        else:
            print(f"  ✅ Diretório será criado: {DATA_DIR}")
        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


def test_dependencies():
    """Testa se as dependências estão instaladas."""
    print("\n🔍 Testando dependências...")
    
    dependencies = {
        "requests": "requests",
        "urwid": "urwid",
        "google.genai": "google-genai",
        "dotenv": "python-dotenv"
    }
    
    all_ok = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Execute: pip install {package}")
            all_ok = False
    
    return all_ok


def main():
    """Executa todos os testes."""
    print("=" * 70)
    print("🧪 R.A.F.F - Teste de Configuração")
    print("=" * 70)
    
    tests = [
        ("Dependências", test_dependencies),
        ("Arquivo .env", test_env),
        ("Imports de módulos", test_imports),
        ("Diretório de dados", test_data_dir),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erro ao executar teste '{name}': {e}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 Todos os testes passaram! O R.A.F.F está pronto para uso.")
        print("\nPara executar: python -m src.main")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Corrija os problemas acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
