from setuptools import setup, find_packages

# Lê requirements.txt automaticamente
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="raff",
    version="1.2.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "raff=src.cli.commands:main",
        ],
    },
    install_requires=requirements,
    python_requires=">=3.8",
)