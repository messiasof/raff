from setuptools import setup, find_packages

# Lê requirements.txt automaticamente
with open("requirements.txt") as f:
    requirements = [
        line.strip() 
        for line in f 
        if line.strip() and not line.strip().startswith("#") # Segurança caso no futuro o comportamento do line.strip() mude e quebre a lógica
    ]

setup(
    name="raff",
    version="1.3.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "raff=src.cli.commands:mainCLI",
            "raff-warn=src.warn:main",
        ],
    },
    install_requires=requirements,
    python_requires=">=3.8",
)