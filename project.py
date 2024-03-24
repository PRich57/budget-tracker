import json
from colorama import Fore
from datetime import datetime
from tabulate import tabulate

# I'll modularize into more practical file structure after
# submitting in the required format for the final project of CS50P
# I'm adding potential filenames above each function so I can easily move them when the time comes

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
            print(Fore.YELLOW + "\nExiting the budget tracker.")
            break
        else:
            print(Fore.RED + "\nInvalid choice. Please choose again.")


# main_menu.py
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


# helpers.py
def load_transactions():
    # Load transactions from a JSON file, return an empty list if file doesn't exist
    try:
        with open('transactions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

# helpers.py
def save_transactions(transactions):
    # Save transactions to a JSON file
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file, indent=4)


# main_menu.py
def add_transaction():
    # Add a new transaction after gathering input from the user
    transactions = load_transactions()
    # new_id = 1 if not transactions else transactions[-1]['id'] + 1
    date = get_valid_date()
    description = input("Enter the transaction description: ")
    type = get_type()
    amount = get_valid_amount()
    transaction = {
        # 'id': new_id,
        'date': date,
        'description': description,
        'type': type,
        'amount': amount
    }
    transactions.append(transaction)
    # Sort chronologically
    transactions.sort(key=lambda x: x['date'])
    save_transactions(transactions)
    print(Fore.GREEN + "\nTransaction added successfully.")


# helpers.py
def get_valid_date(date_input=None):
    # Ensure the date provided is in the proper format
    while True:
        if date_input is None:
            date_input = input(Fore.CYAN + "\nEnter the date (YYYY-MM-DD): ").strip()
        try:
            valid_date = datetime.strptime(date_input, '%Y-%m-%d')
            return valid_date.strftime('%Y-%m-%d')
        except ValueError:
            print(Fore.RED + "\nInvalid date format. Please ender a date in the format YYYY-MM-DD.")
            # Reset to prompt again
            date_input = None

# helpers.py
def get_type(type_input=None):
    # Declare variable and assign list of valid types
    valid_types = ['income', 'expense']
    # Type is important to validate for the report, so another menu is displayed
    while True:
        if type_input is None or type_input not in valid_types:
            display_type_menu()
            choice = input(Fore.CYAN + "Enter your choice: ").strip()

            if choice in valid_types:
                return choice
            elif choice == '1':
                return 'income'
            elif choice == '2':
                return 'expense'
            else:
                print(Fore.RED + "\nInvalid choice. Please choose again.")
                # Reset type_input to prompt again
                type_input = None
        else:
            return type_input


# helpers.py
def display_type_menu():
    # Menu for the type of transaction
    print(Fore.CYAN + """
    1 - Income
    2 - Expense
    """)


# helpers.py
def get_valid_amount(amount_input=None):
    # Ensure the validity of the user provided amount
    while True:
        if amount_input is None:
            amount_input = input(Fore.CYAN + "Amount: ").strip()
        try:
            amount = float(amount_input)
            return amount
        except ValueError:
            print(Fore.RED + "\nInvalid amount. Please enter a numeric value.\n")
            # Reset to prompt again
            amount_input = None


# main_menu.py
def view_transactions():
    # Display all transactions
    transactions = load_transactions()
    table_data = []
    # Check if there are any transactions to display
    if transactions:
        for i, transaction in enumerate(transactions, start=1):
            # Color code based on transaction type
            color = Fore.RED if transaction['type'] == 'expense' else Fore.GREEN
            # Apply color to entire row
            row = [
                color + f"{i}" + Fore.CYAN,
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
        # print(Fore.RED + "\nNo transactions found.")
        print(tabulate(table_data, headers=['ID', 'Date', 'Description', 'Type', 'Amount'], tablefmt="grid"))


# main_menu.py
def update_transaction():
    # print(Fore.GREEN + "\nUpdate transaction placeholder")
    view_transactions()

    transactions = load_transactions()
    if transactions:
        transaction_id_to_update = input(Fore.CYAN + "\nEnter the ID of the transaction you wish to update, or 'Q' to cancel: ").strip().lower()

        if transaction_id_to_update.lower() == 'q':
            print(Fore.YELLOW + "\nUpdate cancelled. Returning to main menu.")
            return
        
        if not transaction_id_to_update.isdigit() or not 1 <= int(transaction_id_to_update) <= len(transactions):
            print(Fore.RED + "\nInvalid transaction ID.")
            return
        
        # Convert ID to an index
        transaction_id_to_update = int(transaction_id_to_update) - 1
        transaction_to_update = transactions[transaction_id_to_update]

        # Show current values of the transaction
        print(Fore.CYAN + "\nCurrent transaction details:")
        print(tabulate([[key, value] for key, value in transaction_to_update.items()], headers=['Field', 'Current Value'], tablefmt="grid"))

        # Prompt user for updated values or keep original
        new_date = input(f"\nEnter new date (YYYY-MM-DD) or press enter to keep ({transaction_to_update['date']}): ").strip()
        if new_date:
            transaction_to_update['date'] = get_valid_date(new_date)

        new_description = input(f"Enter new description or press enter to keep ({transaction_to_update['description']}): ").strip()
        if new_description:
            transaction_to_update['description'] = new_description

        new_type = input(f"Enter new type (income/expense) or press enter to keep ({transaction_to_update['type']}): ")
        if new_type:
            transaction_to_update['type'] = get_type(new_type)

        new_amount_str = input(f"Enter new amount or press enter to keep (${transaction_to_update['amount']:.2f}): ")
    
        if new_description:
            transaction_to_update['description'] = new_description
        if new_amount_str:
            try:
                new_amount = float(new_amount_str)
                transaction_to_update['amount'] = new_amount
            except ValueError:
                print(Fore.RED + "\nInvalid amount. Keeping the original amount.")

        # Save the updated transaction list
        save_transactions(transactions)
        print(Fore.GREEN + "\nTransaction updated successfully.")
    else:
        print(Fore.RED + "\nNo transactions to update.")


# main_menu.py
def delete_transaction():
    while True:
        # Call view_transactions to show user the organized data
        view_transactions()

        transactions = load_transactions()
        if transactions:
            # Prompt user for ID of the transaction they wish to delete
            user_input = input(Fore.CYAN + "\nEnter the ID of the transaction you wish to delete, or 'Q' to cancel: ").strip().lower()
            # Provide user with a way to return to main menu if they no longer want to delete
            if user_input == 'q':
                print(Fore.YELLOW + "\nDeletion cancelled. Returning to the main menu.")
                break

            try:
                transaction_id_to_delete = int(user_input)
                # Validate
                if 1 <= transaction_id_to_delete <= len(transactions):
                    # Delete the transaction, subtracting 1 due to IDs starting at 1 instead of 0
                    del transactions[transaction_id_to_delete - 1]
                    save_transactions(transactions)
                    print(Fore.GREEN + "\nTransaction deleted successfully.")
                    break
                else:
                    # Invalid ID error message
                    print(Fore.RED + "\nInvalid ID. Please try again.")
            except ValueError:
                # User entered non-integer value
                print(Fore.RED + "\nInvalid input. Please enter a numeric ID.")
        else:
            # No transactions to delete
            print(Fore.RED + "\nNo transactions to delete.")
            break


# main_menu.py
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