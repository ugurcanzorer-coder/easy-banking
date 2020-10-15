# Write your code here
import random
import sys
import sqlite3


class Customer:
    def __init__(self, card_no, password):
        self.card_no = card_no
        self.password = password

    def __str__(self):
        return "Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}"\
            .format(self.card_no, self.password)


def luhn_algorithm(card_no):
    result = 0
    check = 0
    for each in card_no:
        check += 1
        each = int(each)
        if check % 2 == 1 and each != 9:
            each = (each * 2) % 9
        result += each
    if result % 10 == 0:
        return True
    print("Probably you made a mistake in the card number.\nPlease try again!")


def card_generator():
    card_no = "400000"
    result = 0
    check = 0
    for each in range(9):
        card_no = card_no + str(random.randint(0, 9))
    for each in card_no:
        check += 1
        each = int(each)
        if check % 2 == 1 and each != 9:
            each = (each * 2) % 9
        result += each
    card_no = card_no + str((result * 9) % 10)
    return card_no


class Bank:
    def __init__(self):
        self.connection()

    def connection(self):
        self.conn = sqlite3.connect("card.s3db")

        self.cur = self.conn.cursor()

        query = "CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, 'number' TEXT," \
                " pin TEXT, balance INTEGER DEFAULT 0)"

        self.cur.execute(query)
        self.conn.commit()

    def disconnect(self):
        self.conn.close()

    def create(self):

        card_no = card_generator()
        password = str(random.randint(0, 9999)).zfill(4)

        query = "INSERT INTO card(number, pin) VALUES(?, ?)"

        self.cur.execute(query, (card_no, password))

        self.conn.commit()

        customer = Customer(card_no, password)

        return customer

    def login(self, card_no, password):
        if luhn_algorithm(card_no):

            query = "SELECT * FROM card WHERE number = ? AND pin = ?"

            self.cur.execute(query, (card_no, password))

            card = self.cur.fetchall()
            if len(card) == 0:
                print("Wrong card number or PIN!")
            else:
                customer = Customer(card[0][1], card[0][2])
                return customer

    def balance(self, card_no):
        query = "SELECT balance FROM card WHERE number = ?"

        self.cur.execute(query, (card_no,))

        account_balance = self.cur.fetchone()

        print("Balance: {}".format(account_balance))

        return account_balance

    def add_income(self, add, card_no):
        query = "UPDATE card SET balance = balance + ? WHERE number = ?"

        self.cur.execute(query, (add, card_no))

        self.conn.commit()

    def transfer(self, card_no):
        if luhn_algorithm(card_no):
            if card_no != customer.card_no:
                query = "SELECT balance FROM card WHERE number = ?"

                self.cur.execute(query, (card_no,))

                transfered_account = self.cur.fetchone()

                if transfered_account:
                    transfer_money = int(input("Enter how much money you want to transfer:"))
                    customer_account_balance = self.balance(customer.card_no)
                    if transfer_money < customer_account_balance[0]:
                        query = "UPDATE card SET balance = balance - ? WHERE number = ?"

                        self.cur.execute(query, (transfer_money, customer.card_no))
                        self.conn.commit()

                        query = "UPDATE card SET balance = balance + ? WHERE number = ?"

                        self.cur.execute(query, (transfer_money, card_no))
                        self.conn.commit()
                        print("Success!")

                    else:
                        print("Not enough money!")
                else:
                    print("Such a card does not exist.")
            else:
                print("You can't transfer money to the same account")

    def close_account(self):
        query = "DELETE FROM card WHERE number = ?"

        self.cur.execute(query, (customer.card_no,))

        self.conn.commit()
        print("The account has been closed!")

bank = Bank()
while True:
    checkpoint1 = input("""
1. Create an account
2. Log into account
0. Exit
""")

    if checkpoint1 == "1":
        customer = bank.create()
        print(customer)

    elif checkpoint1 == "2":
        card_no = input("Enter your card number:")
        password = input("Enter your password:")
        customer = bank.login(card_no, password)
        if customer:
            print("You have successfully logged in!")
            while True:
                checkpoint2 = input("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
                if checkpoint2 == "1":
                    bank.balance(customer.card_no)
                elif checkpoint2 == "2":
                    add = int(input("Enter income: "))
                    bank.add_income(add, customer.card_no)
                    print("Income was added!")
                elif checkpoint2 == "3":
                    card_no = input("Transfer\nEnter card number: ")
                    bank.transfer(card_no)
                elif checkpoint2 == "4":
                    bank.close_account()
                    break
                elif checkpoint2 == "5":
                    print("You have successfully logged out!")
                    break
                elif checkpoint2 == "0":
                    bank.disconnect()
                    print("Bye!")
                    sys.exit()
                else:
                    print("Wrong action")
    elif checkpoint1 == "0":
        bank.disconnect()
        print("Bye!")
        sys.exit()
    else:
        print("Wrong action")
