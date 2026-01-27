from colorama import Fore, Style

def log_info(msg: str):
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {msg}")

def log_success(msg: str):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")

def log_error(msg: str):
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")
