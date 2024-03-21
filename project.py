import json
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
            print("Exiting the budget tracker.")
            break
        else:
            print("Invalid choice. Please choose again.")


def display_menu():
    # Display the user menu
    print("""
    Budget Tracker Menu:
    1 - Add Transaction
    2 - View Transactions
    3 - Update Transaction
    4 - Delete Transaction
    5 - Generate Report
    Q/q - Quit
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
    with open('transaction.json', 'w') as file:
        json.dump(transactions, file, indent=4)


def add_transaction():
    # Add a new transaction after gathering input from the user
    transactions = load_transactions()
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Enter the transaction description: ")
    type = input("Type (income/expense): ")
    amount = float(input("Amount: "))
    transaction = {
        'date': date,
        'description': description,
        'type': type,
        'amount': amount
    }
    transactions.append(transaction)
    save_transactions(transactions)
    print("Transaction added successfully.")


# def view_transactions():
    



# def update_transaction():




# def delete_transaction():



# def generate_report():
    

if __name__ == "__main__":
    main()