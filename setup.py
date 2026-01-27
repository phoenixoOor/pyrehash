from setuptools import setup, find_packages

setup(
    name="pyrehash",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.9.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "pyyaml>=6.0",
        "colorama>=0.4.6",
        "tqdm>=4.65.0",
        "passlib>=1.7.4",
        "bcrypt>=4.0.1",
        "argon2-cffi>=21.1.0",
        "requests>=2.31.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "pyrehash=src.cli.commands:app",
        ],
    },
    python_requires=">=3.9",
)
