from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [
        line.strip() 
        for line in f 
        if line.strip() and not line.strip().startswith("#")
    ]

setup(
    name="raff",
    version="2.0.0",
    description="Rotina de Aprendizado Focada e Flexível",
    author="Emanuel Messias",
    author_email="contato@messias.me",
    url="https://messias.me",
    packages=find_packages(where="."),
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "raff=raff.cli.commands:mainCLI",
            "raff-warn=raff.warn:main",
        ],
    },
    install_requires=requirements,
    python_requires=">=3.8",
)
