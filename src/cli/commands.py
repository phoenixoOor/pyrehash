import typer
from typing import Optional
from .banner import get_banner
from ..core.hash_utils import detect_algorithm
from ..attacks.dictionary_attack import DictionaryAttack
from ..attacks.brute_force_attack import BruteForceAttack
from ..attacks.hybrid_attack import HybridAttack
from ..database.storage import Storage
from ..utils.color_output import log_info, log_success, log_error
from ..utils.benchmark import run_benchmark

app = typer.Typer(help="Professional Hash Cracker")
storage = Storage()

@app.command()
def benchmark(
    algorithm: str = typer.Argument(..., help="Algorithm to benchmark")
):
    """Run a performance benchmark for an algorithm."""
    run_benchmark(algorithm)

@app.command()
def server(
    host: str = "127.0.0.1",
    port: int = 8000
):
    """Start the REST API server."""
    import uvicorn
    from ..api.main import app as fastapi_app
    log_info(f"Starting server at {host}:{port}")
    uvicorn.run(fastapi_app, host=host, port=port)

@app.command()
def crack(
    target: str = typer.Option(..., "--target", "-t", help="Target hash"),
    mode: str = typer.Option(..., "--mode", "-m", help="Attack mode: dict or brute"),
    algorithm: Optional[str] = typer.Option(None, "--algorithm", "-a", help="Hash algorithm"),
    dictionary: Optional[str] = typer.Option(None, "--file", "-f", help="Dictionary file path"),
    length: Optional[int] = typer.Option(None, "--length", "-l", help="Max password length"),
    charset: str = typer.Option("lower", "--charset", "-c", help="Charset preset or literal"),
    salt: Optional[str] = typer.Option(None, "--salt", help="Salt value"),
    salt_pos: str = typer.Option("prefix", "--salt-position", help="Salt position: prefix or suffix"),
):
    """Start a cracking session."""
    print(get_banner())
    
    if not algorithm:
        algorithm = detect_algorithm(target)
        if algorithm:
            log_info(f"Detected algorithm: {algorithm}")
        else:
            log_error("Could not detect algorithm. Please specify with -a.")
            raise typer.Exit(code=1)

    try:
        if mode == "dict":
            if not dictionary:
                log_error("Dictionary mode requires a file (-f).")
                raise typer.Exit(code=1)
            
            engine = DictionaryAttack(target, algorithm)
            result = engine.run(dictionary, salt, salt_pos)
            
        elif mode == "hybrid":
            if not dictionary:
                log_error("Hybrid mode requires a dictionary file (-f).")
                raise typer.Exit(code=1)
            
            engine = HybridAttack(target, algorithm)
            result = engine.run(dictionary, salt, salt_pos)

        elif mode == "brute":
            if length is None:
                log_error("Brute-force mode requires a length (-l).")
                raise typer.Exit(code=1)
            
            # Map presets
            presets = {
                "lower": "abcdefghijklmnopqrstuvwxyz",
                "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "digits": "0123456789",
                "all": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            }
            charset_str = presets.get(charset, charset)
            
            engine = BruteForceAttack(target, algorithm)
            result = engine.run(charset_str, 1, length, salt, salt_pos)
        else:
            log_error(f"Unknown mode: {mode}")
            raise typer.Exit(code=1)

        if result:
            log_success(f"Password found: {result}")
            storage.save_result(target, result)
        else:
            log_error("Password not found.")
            
        log_info(f"Attempts: {engine.attempts}")
        log_info(f"Speed: {engine.speed:.2f} H/s")
        log_info(f"Elapsed: {engine.elapsed_time:.2f}s")

    except Exception as e:
        log_error(f"Error: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def list_results():
    """List found passwords from the database."""
    from ..database.models import HashTarget, Result
    with storage.Session() as session:
        results = session.query(Result).all()
        if not results:
            print("No results found.")
            return
        for r in results:
            print(f"Hash: {r.target.hash_value} | Password: {r.password}")

@app.command()
def clear_results():
    """Clear all results and targets from the database."""
    if typer.confirm("Are you sure you want to clear all results?"):
        storage.clear_results()
        log_success("Database cleared.")

if __name__ == "__main__":
    app()
