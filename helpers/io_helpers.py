import json
from pathlib import Path

from colorama import Fore


def load_transactions() -> list[dict]:
    # Load transactions from JSON file, return an empty list if file doesn't exist or is corrupted
    try:
        with Path('transactions.json').open('r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Fore.YELLOW}\nTransaction file not found. Starting with an empty list.\n{Fore.CYAN}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}\nTransaction file is corrupted. Starting with an empty list.\n{Fore.CYAN}")
        return []
    except Exception as e:
        print(f"{Fore.RED}\nAn error occurred while loading transactions: {e}\n{Fore.CYAN}")
        return []


def save_transactions(transactions: list[dict]) -> None:
    # Save transactions to a JSON file
    try:
        with Path('transactions.json').open('w') as file:
            json.dump(transactions, file, indent=4)
    except Exception as e:
        print(f"{Fore.RED}\nAn error occurred while saving transactions: {e}\n{Fore.CYAN}")