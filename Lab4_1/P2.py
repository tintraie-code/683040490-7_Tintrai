from Bank import BankAccount

# Create accounts
john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1_000_000)
sarah_saving = BankAccount("Sarah")

# Activities
# John deposits 3,000
john.deposit(3000)

# Tim pays half of loan
tim.pay_loan(-tim.balance / 2)

# Sarah deposits 50,000,000
sarah_saving.deposit(50_000_000)

# Sarah opens another loan account
sarah_loan = BankAccount("Sarah", "loan", -100_000_000)

# Show all accounts
accounts = [john, tim, sarah_saving, sarah_loan]

for acc in accounts:
    acc.print_customer()
