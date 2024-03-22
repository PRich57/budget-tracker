import json
from colorama import Fore
from datetime import datetime
from tabulate import tabulate

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
    new_id = 1 if not transactions else transactions[-1]['id'] + 1
    date = get_valid_date()
    description = input("Enter the transaction description: ")
    type = get_type()
    amount = get_valid_amount()
    transaction = {
        'id': new_id,
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
        choice = input(Fore.CYAN + "Enter your choice: ").strip()
        if choice == '1':
            return 'income'
        elif choice == '2':
            return 'expense'
        else:
            print(Fore.RED + "\nInvalid choice. Please choose again.")


def display_type_menu():
    # Menu for the type of transaction
    print(Fore.CYAN + """
    1 - Income
    2 - Expense
    """)


def get_valid_amount():
    # Ensure the validity of the user provided amount
    while True:
        try:
            amount = float(input(Fore.CYAN + "Amount: "))
            return amount
        except ValueError:
            print(Fore.RED + "\nInvalid amount. Please enter a numeric value.\n")


def get_valid_date():
    # Ensure the date provided is in the proper format
    while True:
        date_input = input(Fore.CYAN + "\nEnter the date (YYYY-MM-DD): ")
        try:
            valid_date = datetime.strptime(date_input, '%Y-%m-%d')
            return valid_date.strftime('%Y-%m-%d')
        except ValueError:
            print(Fore.RED + "\nInvalid date format. Please ender a date in the format YYYY-MM-DD.")


def view_transactions():
    # Display all transactions
    transactions = load_transactions()
    # Check if there are any transactions to display
    if transactions:
        table_data = []
        for transaction in transactions:
            # Color code based on transaction type
            color = Fore.RED if transaction['type'] == 'expense' else Fore.GREEN
            # Apply color to entire row
            row = [
                color + f"{transaction['id']}" + Fore.CYAN,
                color + transaction['date'] + Fore.CYAN,
                color + transaction['description'] + Fore.CYAN,
                color + transaction['type'] + Fore.CYAN,
                color + '${:,.2f}'.format(transaction['amount']) + Fore.CYAN
            ]
            # Append list of transaction details
            table_data.append(row)
        # Print with tabulate
        print(Fore.CYAN + "\n" + tabulate(table_data, headers=['ID', 'Date', 'Description', 'Type', 'Amount'], tablefmt="grid"))
    else:
        print(Fore.RED + "No transactions found.")


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

    report_data = [
        [Fore.GREEN + 'Total Income' + Fore.CYAN, Fore.GREEN + f"${income:.2f}" + Fore.CYAN],
        [Fore.RED + 'Total Expense' + Fore.CYAN, Fore.RED + f"${expense:.2f}" + Fore.CYAN],
        ['Net', f"${net:.2f}"]
    ]

    # Conditional coloring for 'Net' based on its value
    net_color = Fore.GREEN if net > 0 else Fore.RED
    # Apply coloring to 'Net'
    report_data[2] = [net_color + 'Net' + Fore.CYAN, net_color + f"${net:.2f}" + Fore.CYAN]
    print(tabulate(report_data, tablefmt="grid"))


if __name__ == "__main__":
    main()