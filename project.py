# import re # Remove after graded and moved back to validation_helpers.py

from colorama import Fore
# from datetime import datetime # Remove after graded and moved back to validation_helpers.py
from tabulate import tabulate

from helpers.io_helpers import load_transactions, save_transactions
# Add the below line back in after graded and validation_helpers.py is used again
from helpers.validation_helpers import get_valid_date, get_valid_type, get_valid_amount


def main():
    # Main loop to display the menu and handle user input
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            handle_add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            handle_update_transaction()
        elif choice == '4':
            handle_delete_transaction()
        elif choice == '5':
            generate_report()
        elif choice.lower() == 'q':
            print(Fore.YELLOW + "\nExiting the budget tracker.")
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
        q - Quit
    """)


# Refactored for testing
def add_transaction(transactions, date, description, type, amount):
    transaction = {
        'date': date,
        'description': description,
        'type': type,
        'amount': amount
    }
    transactions.append(transaction)
    transactions.sort(key=lambda x: x['date'])
    save_transactions(transactions)
    print(Fore.GREEN + "\nTransaction added successfully.")


# Refactored for testing
def handle_add_transaction():
    transactions = load_transactions()
    date = get_valid_date()
    description = input("Enter the transaction description: ")
    type = get_valid_type()
    amount = get_valid_amount()

    add_transaction(transactions, date, description, type, amount)


# def add_transaction():
#     # Add a new transaction after gathering input from the user
#     transactions = load_transactions()
#     # new_id = 1 if not transactions else transactions[-1]['id'] + 1
#     date = get_valid_date()
#     description = input("Enter the transaction description: ")
#     type = get_valid_type()
#     amount = get_valid_amount()
#     transaction = {
#         # 'id': new_id,
#         'date': date,
#         'description': description,
#         'type': type,
#         'amount': amount
#     }
#     transactions.append(transaction)
#     # Sort chronologically
#     transactions.sort(key=lambda x: x['date'])
#     save_transactions(transactions)
#     print(Fore.GREEN + "\nTransaction added successfully.")


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


# Refactored for testing
def update_transaction(transactions, transaction_id, new_date=None, new_description=None, new_type=None, new_amount=None):
    if not 0 <= transaction_id < len(transactions):
        print(Fore.RED + "\nInvalid transaction ID.")
        return False
    
    if new_date:
        transactions[transaction_id]['date'] = new_date
    if new_description:
        transactions[transaction_id]['description'] = new_description
    if new_type:
        transactions[transaction_id]['type'] = new_type
    if new_amount:
        transactions[transaction_id]['amount'] = new_amount

    transactions.sort(key=lambda x: x['date'])
    save_transactions(transactions)
    print(Fore.GREEN + "\nTransaction updated successfully.")
    return True


# Refactored for testing
def handle_update_transaction():
    transactions = load_transactions()
    if not transactions:
        print(Fore.RED + "\nNo transactions to update.")
        return

    view_transactions()
    transaction_id_str = input("\nEnter the ID of the transaction you wish to update, or 'q' to cancel: ").strip().lower()
    if transaction_id_str.lower() == 'q':
        print(Fore.YELLOW + "\nUpdate cancelled. Returning to the main menu.")
        return
    
    if not transaction_id_str.isdigit() or not 1 <= int(transaction_id_str) <= len(transactions):
        print(Fore.RED + "\nInvalid transaction ID.")
        return

    transaction_id = int(transaction_id_str) - 1
    transaction_to_update = transactions[transaction_id]

    new_date = input(f"\nEnter new date (YYYY-MM-DD) or press enter to keep ({transaction_to_update['date']}): ").strip()
    transaction_to_update['date'] = get_valid_date(new_date) if new_date else transaction_to_update['date']

    new_description = input(f"Enter new description or press enter to keep ({transaction_to_update['description']}): ").strip()
    transaction_to_update['description'] = new_description if new_description else transaction_to_update['description']
    
    new_type = input(f"Enter new type (income/expense) or press enter to keep ({transaction_to_update['type']}): ").strip().lower()
    transaction_to_update['type'] = get_valid_type(new_type) if new_type else transaction_to_update['type']
    
    new_amount_str = input(f"Enter new amount or press enter to keep (${transaction_to_update['amount']:.2f}): ").strip()
    transaction_to_update['amount'] = get_valid_amount(new_amount_str) if new_amount_str else transaction_to_update['amount']

    update_transaction(transactions, transaction_id, transaction_to_update['date'], transaction_to_update['description'], transaction_to_update['type'], transaction_to_update['amount'])


# def update_transaction():
#     view_transactions()

#     transactions = load_transactions()
#     if transactions:
#         transaction_id_to_update = input(Fore.CYAN + "\nEnter the ID of the transaction you wish to update, or 'Q' to cancel: ").strip().lower()

#         if transaction_id_to_update.lower() == 'q':
#             print(Fore.YELLOW + "\nUpdate cancelled. Returning to main menu.")
#             return
        
#         if not transaction_id_to_update.isdigit() or not 1 <= int(transaction_id_to_update) <= len(transactions):
#             print(Fore.RED + "\nInvalid transaction ID.")
#             return
        
#         # Convert ID to an index
#         transaction_id_to_update = int(transaction_id_to_update) - 1
#         transaction_to_update = transactions[transaction_id_to_update]

#         # Show current values of the transaction
#         print(Fore.CYAN + "\nCurrent transaction details:")
#         print(tabulate([[key, value] for key, value in transaction_to_update.items()], headers=['Field', 'Current Value'], tablefmt="grid"))

#         # Prompt user for updated values or keep original
#         new_date = input(f"\nEnter new date (YYYY-MM-DD) or press enter to keep ({transaction_to_update['date']}): ").strip()
#         # Validate and update transaction
#         transaction_to_update['date'] = get_valid_date(new_date) if new_date else transaction_to_update['date']

#         new_description = input(f"Enter new description or press enter to keep ({transaction_to_update['description']}): ").strip()
#         transaction_to_update['description'] = new_description if new_description else transaction_to_update['description']
        
#         new_type = input(f"Enter new type (income/expense) or press enter to keep ({transaction_to_update['type']}): ").strip().lower()
#         transaction_to_update['type'] = get_valid_type(new_type) if new_type else transaction_to_update['type']
        
#         new_amount_str = input(f"Enter new amount or press enter to keep (${transaction_to_update['amount']:.2f}): ").strip()
#         transaction_to_update['amount'] = get_valid_amount(new_amount_str) if new_amount_str else transaction_to_update['amount']

#         # Sort and save the updated transaction list
#         transactions.sort(key=lambda x: x['date'])
#         save_transactions(transactions)
#         print(Fore.GREEN + "\nTransaction updated successfully.")
#     else:
#         print(Fore.RED + "\nNo transactions to update.")


# Refactored for testing
def delete_transaction(transactions, transaction_id):
    # Delete transaction with provided ID from the transactions list
    del transactions[transaction_id]
    # Save updated list
    save_transactions(transactions)
    print(Fore.GREEN + "\nTransaction deleted successfully.")
    return True


# Refactored for testing
def handle_delete_transaction():
    transactions = load_transactions()
    if not transactions:
        print(Fore.RED + "\nNo transactions to delete.")
        return

    # Call view_transactions to show user the organized data
    view_transactions()
    # Prompt user for the ID of the transaction they wish to delete
    transaction_id_str = input(Fore.CYAN + "\nEnter the ID of the transaction you wish to delete, or 'q' to cancel: ").strip().lower()

    # Provide user with a way to return to the main menu
    if transaction_id_str.lower() == 'q':
        print(Fore.YELLOW + "\nDeletion cancelled. Returning to the main menu.")
        return
    
    # Send error message and return to main menu when invalid ID is provided
    if not transaction_id_str.isdigit() or not 1 <= int(transaction_id_str) <= len(transactions):
        print(Fore.RED + "\nInvalid transaction ID.")
        return
    
    # Convert user provided transaction ID to an int and subtract 1 to align with 0 indexing
    transaction_id = int(transaction_id_str) - 1

    # Confirm deletion with user
    confirm = input(Fore.YELLOW + "\nAre you sure you want to delete this transaction? (y/n): ").strip().lower()
    if confirm == 'y':
        delete_transaction(transactions, transaction_id)
    else:
        print(Fore.YELLOW + "\nDeletion cancelled.")


# def delete_transaction():
#     while True:
#         # Call view_transactions to show user the organized data
#         view_transactions()

#         transactions = load_transactions()
#         if transactions:
#             # Prompt user for ID of the transaction they wish to delete
#             user_input = input(Fore.CYAN + "\nEnter the ID of the transaction you wish to delete, or 'Q' to cancel: ").strip().lower()
#             # Provide user with a way to return to main menu if they no longer want to delete
#             if user_input == 'q':
#                 print(Fore.YELLOW + "\nDeletion cancelled. Returning to the main menu.")
#                 break

#             try:
#                 transaction_id_to_delete = int(user_input)
#                 # Validate
#                 if 1 <= transaction_id_to_delete <= len(transactions):
#                     # Delete the transaction, subtracting 1 due to IDs starting at 1 instead of 0
#                     del transactions[transaction_id_to_delete - 1]
#                     save_transactions(transactions)
#                     print(Fore.GREEN + "\nTransaction deleted successfully.")
#                     break
#                 else:
#                     # Invalid ID error message
#                     print(Fore.RED + "\nInvalid ID. Please try again.")
#             except ValueError:
#                 # User entered non-integer value
#                 print(Fore.RED + "\nInvalid input. Please enter a numeric ID.")
#         else:
#             # No transactions to delete
#             print(Fore.RED + "\nNo transactions to delete.")
#             break


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


# The functions below were moved back into project.py for the sake of unit test grading requirements
# Comment the validation_helpers file back in and remove these from this file after grading is complete
# def get_valid_date(date_input=None):
#     # Validate or get a date from the user
#     while True:
#         # Prompt for date if date_input is None
#         if date_input is None:
#             date_input = input(Fore.CYAN + "\nEnter the date (YYYY-MM-DD): ").strip()

#         # Check if the date is valid
#         if is_valid_date(date_input):
#             return date_input
#         else:
#             # Reset to loop back through until valid date is provided
#             date_input = None


# def is_valid_date(date_str):
#     # Check if date string matches strict format
#     if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
#         try:
#             # Ensure date string is an actual date
#             datetime.strptime(date_str, '%Y-%m-%d')
#             return True
#         except ValueError:
#             print(Fore.RED + "\nInvalid date. Please enter a valid date in the format YYYY-MM-DD.")
#             return False
#     # Return False if the date doesn't match the correct format
#     print(Fore.RED + "\nInvalid date format. Please enter a date in the format YYYY-MM-DD.")
#     return False


# def get_valid_type(type_input=None):
#     # Validate or get the transaction type from the user
#     valid_types = ['income', 'expense']
#     while True:
#         if type_input is None or type_input not in valid_types:
#             display_type_menu()
#             type_input = input(Fore.CYAN + "Enter your choice: ").strip()
#             type_input = 'income' if type_input == '1' else 'expense' if type_input == '2' else None
#         if type_input in valid_types:
#             return type_input
#         else:
#             print(Fore.RED + "\nInvalid choice. Please choose again.")
#             type_input = None


# def display_type_menu():
#     # Menu for the type of transaction
#     print(Fore.CYAN + """
#     1 - Income
#     2 - Expense
#     """)


# def get_valid_amount(amount_input=None):
#     # Validate or get the amount from the user
#     while True:
#         if amount_input is None or not is_valid_amount(amount_input):
#             amount_input = input(Fore.CYAN + "Amount: ").strip()
#         else:
#             return float(amount_input)


# def is_valid_amount(amount_str):
#     # Ensure amount string is a valid float
#     try:
#         float(amount_str)
#         return True
#     except ValueError:
#         print(Fore.RED + "\nInvalid amount. Please enter a numeric value.")
#         return False


if __name__ == "__main__":
    main()