from colorama import Fore
from datetime import datetime


def get_valid_date(date_input=None):
    # Validate or get a date from the user
    while True:
        if date_input is None or not is_valid_date(date_input):
            date_input = input(Fore.CYAN + "\nEnter the date (YYYY-MM-DD): ").strip()
        else:
            return date_input


def is_valid_date(date_str):
    # Ensure date string is in proper format
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        print(Fore.RED + "\nInvalid date format. Please enter a date in the format YYYY-MM-DD.")
        return False


def get_valid_type(type_input=None):
    # Validate or get the transaction type from the user
    valid_types = ['income', 'expense']
    while True:
        if type_input is None or type_input not in valid_types:
            display_type_menu()
            type_input = input(Fore.CYAN + "Enter your choice: ").strip()
            type_input = 'income' if type_input == '1' else 'expense' if type_input == '2' else None
        if type_input in valid_types:
            return type_input
        else:
            print(Fore.RED + "\nInvalid choice. Please choose again.")


def display_type_menu():
    # Menu for the type of transaction
    print(Fore.CYAN + """
    1 - Income
    2 - Expense
    """)


def get_valid_amount(amount_input=None):
    # Validate or get the amount from the user
    while True:
        if amount_input is None or not is_valid_amount(amount_input):
            amount_input = input(Fore.CYAN + "Amount: ").strip()
        else:
            return float(amount_input)


def is_valid_amount(amount_str):
    # Ensure amount string is a valid float
    try:
        float(amount_str)
        return True
    except ValueError:
        print(Fore.RED + "\nInvalid amount. Please enter a numeric value.")
        return False