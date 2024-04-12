import json

from colorama import Fore


def load_transactions():
    # Load transactions from JSON file, return an empty list if file doesn't exist or is corrupted
    try:
        with open('transactions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(Fore.YELLOW + "\nTransaction file not found. Starting with an empty list.\n" + Fore.CYAN)
        return []
    except json.JSONDecodeError:
        print(Fore.RED + "\nTransaction file is corrupted. Starting with an empty list.\n" + Fore.CYAN)
        return []
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred while loading transactions: {e}\n" + Fore.CYAN)
        return []


def save_transactions(transactions):
    # Save transactions to a JSON file
    try:
        with open('transactions.json', 'w') as file:
            json.dump(transactions, file, indent=4)
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred while saving transactions: {e}\n" + Fore.CYAN)