import json
from colorama import Fore
from datetime import datetime

def main():
    # Main loop to display the menu and handle user input
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            generate_report()
        elif choice.lower() == 'q':
            print(Fore.GREEN + "\nExiting the budget tracker.")
            break
        else:
            print(Fore.RED + "\nInvalid choice. Please choose again.")


def display_menu():
    # Display the user menu
    print(Fore.CYAN + """
    Budget Tracker Menu:
    
        1 - Add Transaction
        2 - View Transactions
        3 - Update Transaction
        4 - Delete Transaction
        5 - Generate Report
        Q - Quit
    """)


def load_transactions():
    # Load transactions from a JSON file, return an empty list if file doesn't exist
    try:
        with open('transactions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

def save_transactions(transactions):
    # Save transactions to a JSON file
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file, indent=4)


def add_transaction():
    # Add a new transaction after gathering input from the user
    transactions = load_transactions()
    date = input("\nEnter the date (YYYY-MM-DD): ")
    description = input("Enter the transaction description: ")
    type = get_type()
    amount = float(input("Amount: "))
    transaction = {
        'date': date,
        'description': description,
        'type': type,
        'amount': amount
    }
    transactions.append(transaction)
    save_transactions(transactions)
    print(Fore.GREEN + "\nTransaction added successfully.")


def get_type():
    # Type is important to validate for the report, so another menu is displayed
    while True:
        display_type_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            return 'income'
        elif choice == '2':
            return 'expense'
        else:
            print(Fore.RED + "\nInvalid choice. Please choose again.")


def display_type_menu():
    # Menu for the type of transaction
    print("""
    1 - Income
    2 - Expense
    """)


def view_transactions():
    # Display all transactions
    transactions = load_transactions()
    for transaction in transactions:
        if transaction['type'] == 'expense':
            print(Fore.RED + f"\n{transaction['date']} - {transaction['description']} - {transaction['type']} - {transaction['amount']}")
        else:
            print(Fore.GREEN + f"\n{transaction['date']} - {transaction['description']} - {transaction['type']} - {transaction['amount']}")



def update_transaction():
    print(Fore.GREEN + "\nUpdate transaction placeholder")


def delete_transaction():
    print(Fore.GREEN + "\nDelete transaction placeholder")


def generate_report():
    # Generate and display report of total income, expenses, and net amount
    transactions = load_transactions()
    income = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'income')
    expense = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'expense')
    net = income - expense
    print(Fore.GREEN + f"\nTotal Income: ${income:.2f}")
    print(Fore.RED + f"Total Expense: ${expense:.2f}")
    if net > 0:
        print(Fore.GREEN + f"Net: ${net:.2f}")
    else:
        print(Fore.RED + f"Net: ${net:.2f}")


if __name__ == "__main__":
    main()