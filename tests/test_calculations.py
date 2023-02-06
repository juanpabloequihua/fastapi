import pytest
from app.calculations import add, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,2,9),
    (12,4,16)
    ])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_account(zero_bank_account):
     assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interests(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 55

@pytest.mark.parametrize("deposted, withdrawed, expected", [
    (200,20,180),
    (100,10,90),
    (1200,400,800)
    ])

def test_bank_transaction(zero_bank_account, deposted, withdrawed, expected ):
    zero_bank_account.deposit(deposted)
    zero_bank_account.withdraw(withdrawed)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
