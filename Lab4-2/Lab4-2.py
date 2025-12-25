class BankAccount:
    # class attribute
    branch_name = "Main Branch"

    def __init__(self, acc_no, acc_type, balance):
        self.acc_no = acc_no
        self.acc_type = acc_type      # "saving" or "loan"
        self.balance = balance

    # class method
    @classmethod
    def change_branch_name(cls, new_name):
        cls.branch_name = new_name

    # instance method: deposit (saving only)
    def deposit(self, amount):
        if self.acc_type != "saving":
            print("Deposit allowed for saving account only.")
            return
        self.balance += amount

    # instance method: withdraw (saving only)
    def withdraw(self, amount):
        if self.acc_type != "saving":
            print("Withdraw allowed for saving account only.")
            return
        self.balance -= amount

    # instance method: pay loan (loan only)
    def pay_loan(self, amount):
        if self.acc_type != "loan":
            print("Pay loan allowed for loan account only.")
            return
        self.balance += amount

    # instance method: get loan (loan only)
    def get_loan(self, amount):
        if self.acc_type != "loan":
            print("Get loan allowed for loan account only.")
            return
        if self.balance - amount < -50000:
            print("Loan limit exceeded.")
            return
        self.balance -= amount

    # static method: calculate interest plan
    @staticmethod
    def calc_interest(bal, int_rate, payment):
        year = 1
        print("----- Loan Plan -----")
        while bal > 0:
            loan = bal + (bal * int_rate / 100)

            if loan <= payment:
                payment = loan

            new_bal = loan - payment

            print(
                f"Year {year}: loan = {loan:.2f}  "
                f"payment {payment:.2f}  bal = {new_bal:.2f}"
            )

            bal = new_bal
            year += 1

        print("----- End Plan -----")


# ===== Example usage (optional for testing) =====
if __name__ == "__main__":
    acc1 = BankAccount("001", "saving", 5000)
    acc1.deposit(1000)
    acc1.withdraw(500)
    print(acc1.balance)

    acc2 = BankAccount("002", "loan", -1000)
    acc2.get_loan(2000)
    acc2.pay_loan(500)
    print(acc2.balance)

    BankAccount.calc_interest(1000, 5, 100)
