# The below resources were used to help me understand how to test with mock input:
    # https://docs.python.org/3/library/unittest.mock.html
    # https://docs.pytest.org/en/6.2.x/fixture.html

import pytest

from project import add_transaction, update_transaction, delete_transaction
from unittest.mock import patch


# Mock transaction
@pytest.fixture
def sample_transactions():
    return [
        {'date': '2024-01-01', 'description': 'Test1', 'type': 'income', 'amount': 100},
        {'date': '2024-01-02', 'description': 'Test2', 'type': 'expense', 'amount': 50},
    ]


def test_add_transaction(sample_transactions):
    # Define new transaction to be added
    new_transaction = {'date': '2024-01-03', 'description': 'Test3', 'type': 'income', 'amount': 150}
    expected_transactions = sample_transactions + [new_transaction]

    # Use patch to mock load_transactions and save_transactions
    with patch('project.load_transactions', return_value=sample_transactions), \
        patch('project.save_transactions') as mock_save:

        # Call add_transaction to add new_transaction to the list
        add_transaction(sample_transactions, '2024-01-03', 'Test3', 'income', 150)

        # Assert that 'save_transactions' was called once with the correct list
        mock_save.assert_called_once_with(expected_transactions)


def test_update_transaction(sample_transactions):
    # Define new transaction information to update existing transaction
    updated_transaction = {'date': '2024-01-02', 'description': 'Updated Test2', 'type': 'expense', 'amount': 75}

    with patch('project.load_transactions', return_value=sample_transactions), \
        patch('project.save_transactions') as mock_save:

        # Call update_transaction to update the existing transaction with the new information
        update_transaction(sample_transactions, 1, '2024-01-02', 'Updated Test2', 'expense', 75)

        # Update the expected list to reflect the change
        sample_transactions[1] = updated_transaction

        # Check that save_transactions was called with the updated list
        mock_save.assert_called_once_with(sample_transactions)


def test_delete_transaction(sample_transactions):
    with patch('project.load_transactions', return_value=sample_transactions), \
        patch('project.save_transactions') as mock_save:

        # Remove the first transaction from the expected list
        expected_transactions = sample_transactions[1:]

        # Call delete_transaction to delete the first transaction in the list
        delete_transaction(sample_transactions, 0)

        # Verify save_transactions was called with the correct list after deletion
        mock_save.assert_called_once_with(expected_transactions)