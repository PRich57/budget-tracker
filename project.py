from colorama import Fore
from tabulate import tabulate

from helpers.io_helpers import load_transactions, save_transactions
from helpers.validation_helpers import get_valid_date, get_valid_type, get_valid_amount


def main() -> None:
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
            print(f"{Fore.YELLOW}\nExiting the budget tracker.\n{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}\nInvalid choice. Please choose again.")


def display_menu() -> None:
    # Display the user menu
    print(f"""{Fore.CYAN}
    Budget Tracker Menu:
    
        1 - Add Transaction
        2 - View Transactions
        3 - Update Transaction
        4 - Delete Transaction
        5 - Generate Report
        q - Quit
    """)


def add_transaction(transactions: list[dict], date: str, description: str, type: str, amount: float) -> None:
    transaction = {
        'date': date,
        'description': description,
        'type': type,
        'amount': amount
    }
    transactions.append(transaction)
    transactions.sort(key=lambda x: x['date'])
    save_transactions(transactions)
    print(f"{Fore.GREEN}\nTransaction added successfully.")


def handle_add_transaction() -> None:
    transactions = load_transactions()
    date = get_valid_date()
    description = input("Enter the transaction description: ")
    type = get_valid_type()
    amount = get_valid_amount()

    add_transaction(transactions, date, description, type, amount)


def view_transactions() -> None:
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
                f"{color}{i}{Fore.CYAN}",
                f"{color}{transaction['date']}{Fore.CYAN}",
                f"{color}{transaction['description']}{Fore.CYAN}",
                f"{color}{transaction['type']}{Fore.CYAN}",
                f"{color}${transaction['amount']:,.2f}{Fore.CYAN}"
            ]
            # Append list of transaction details
            table_data.append(row)
        # Print with tabulate
        print(f"{Fore.CYAN}\n{tabulate(table_data, headers=['ID', 'Date', 'Description', 'Type', 'Amount'], tablefmt='grid')}")
    else:
        # print(Fore.RED + "\nNo transactions found.")
        print(tabulate(table_data, headers=['ID', 'Date', 'Description', 'Type', 'Amount'], tablefmt="grid"))


def update_transaction(transactions: list[dict], transaction_id: int,
                       new_date: str | None = None, new_description: str | None = None,
                       new_type: str | None = None, new_amount: float | None = None) -> bool:
    if not 0 <= transaction_id < len(transactions):
        print(f"{Fore.RED}\nInvalid transaction ID.")
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
    print(f"{Fore.GREEN}\nTransaction updated successfully.")
    return True


def handle_update_transaction() -> None:
    transactions = load_transactions()
    if not transactions:
        print(f"{Fore.RED}\nNo transactions to update.")
        return

    view_transactions()
    # Prompt user for for transaction ID or option to return to main menu
    transaction_id_str = input("\nEnter the ID of the transaction you wish to update, or 'q' to cancel: ").strip().lower()
    # Return to main menu if user enters 'q'
    if transaction_id_str.lower() == 'q':
        print(f"{Fore.YELLOW}\nUpdate cancelled. Returning to the main menu.")
        return
    
    # Validation
    if not transaction_id_str.isdigit() or not 1 <= int(transaction_id_str) <= len(transactions):
        print(f"{Fore.RED}\nInvalid transaction ID.")
        return

    # Convert to int and account for change of indexing from 1 to 0
    transaction_id = int(transaction_id_str) - 1
    transaction_to_update = transactions[transaction_id]

    # Give option to enter new date or keep existing
    new_date = input(f"\nEnter new date (YYYY-MM-DD) or press enter to keep ({transaction_to_update['date']}): ").strip()
    transaction_to_update['date'] = get_valid_date(new_date) if new_date else transaction_to_update['date']

    # Give option to enter new description or keep existing
    new_description = input(f"Enter new description or press enter to keep ({transaction_to_update['description']}): ").strip()
    transaction_to_update['description'] = new_description if new_description else transaction_to_update['description']
    
    # Give option to enter new type or keep existing
    new_type = input(f"Enter new type (income/expense) or press enter to keep ({transaction_to_update['type']}): ").strip().lower()
    transaction_to_update['type'] = get_valid_type(new_type) if new_type else transaction_to_update['type']
    
    # Give option to enter new amount or keep existing
    new_amount_str = input(f"Enter new amount or press enter to keep (${transaction_to_update['amount']:.2f}): ").strip()
    transaction_to_update['amount'] = get_valid_amount(new_amount_str) if new_amount_str else transaction_to_update['amount']

    # Call update_transaction function with provided values, new or old
    update_transaction(transactions, transaction_id, transaction_to_update['date'], transaction_to_update['description'], transaction_to_update['type'], transaction_to_update['amount'])


def delete_transaction(transactions: list[dict], transaction_id: int) -> bool:
    # Delete transaction with provided ID from the transactions list
    del transactions[transaction_id]
    # Save updated list
    save_transactions(transactions)
    print(f"{Fore.GREEN}\nTransaction deleted successfully.")
    return True


def handle_delete_transaction() -> None:
    transactions = load_transactions()
    if not transactions:
        print(f"{Fore.RED}\nNo transactions to delete.")
        return

    # Call view_transactions to show user the organized data
    view_transactions()
    # Prompt user for the ID of the transaction they wish to delete
    transaction_id_str = input(f"{Fore.CYAN}\nEnter the ID of the transaction you wish to delete, or 'q' to cancel: ").strip().lower()

    # Provide user with a way to return to the main menu
    if transaction_id_str.lower() == 'q':
        print(f"{Fore.YELLOW}\nDeletion cancelled. Returning to the main menu.")
        return
    
    # Send error message and return to main menu when invalid ID is provided
    if not transaction_id_str.isdigit() or not 1 <= int(transaction_id_str) <= len(transactions):
        print(f"{Fore.RED}\nInvalid transaction ID.")
        return
    
    # Convert user provided transaction ID to an int and subtract 1 to align with 0 indexing
    transaction_id = int(transaction_id_str) - 1

    # Confirm deletion with user
    confirm = input(f"{Fore.YELLOW}\nAre you sure you want to delete this transaction? (y/n): ").strip().lower()
    if confirm == 'y':
        delete_transaction(transactions, transaction_id)
    else:
        print(f"{Fore.YELLOW}\nDeletion cancelled.")


def generate_report() -> None:
    # Generate and display report of total income, expenses, and net amount
    transactions = load_transactions()
    income = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'income')
    expense = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'expense')
    net = income - expense

    report_data = [
        [f"{Fore.GREEN}Total Income{Fore.CYAN}", f"{Fore.GREEN}${income:,.2f}{Fore.CYAN}"],
        [f"{Fore.RED}Total Expense{Fore.CYAN}", f"{Fore.RED}${expense:,.2f}{Fore.CYAN}"],
        ['Net', f"${net:,.2f}"]
    ]

    # Conditional coloring for 'Net' based on its value
    net_color = Fore.GREEN if net > 0 else Fore.RED
    # Apply coloring to 'Net'
    report_data[2] = [f"{net_color}Net{Fore.CYAN}", f"{net_color}${net:,.2f}{Fore.CYAN}"]
    print(tabulate(report_data, tablefmt="grid"))


if __name__ == "__main__":
    main()


# Original add, update, and delete functions

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