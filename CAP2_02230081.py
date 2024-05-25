
################################
# Tandin Wangchuk
# 1st year Electrical department
# 02230081
################################
# REFERENCES
# @https://chat.openai.com/
# @https://www.blackbox.ai/

import random 
import os #The random and OS modules are imported in order to create random numbers for the account and to communicate with the operating system.

#Class Base Account
class Account:
    #Constructor using the appropriate __init__ function
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number  
        self.password = password 
        self.account_type = account_type 
        self.balance = balance 
       # above code is mainly to initiaize account number,password,type and balance 
    # Steps to deposit money or amount
    def deposit(self, amount):
        self.balance += amount  #amount deposited into the account balance 
        print(f"Deposited Ngultrum{amount}. New balance: Ngultrum{self.balance}") #creating a receipt for the deposit
    
    #procedure to withdraw amount
    def withdraw(self, amount):
        if amount > self.balance: #Assessing if the amount of the withdrawal above the balance in the account
            print("Insufficient funds.")# 
        else:
            self.balance -= amount #amount is being subtracted from the withdrawl account balance 
            print(f"Withdraw Ngultrum{amount}. New balance: Ngultrum{self.balance}") # receipt of the withdrawl is being generated
    
    # prcedure for the balance checking
    def check_balance(self):
        return self.balance #Bringing the present balance back

    # amount transferingprocess
    #code below shows the the output if the transfer amount is above or exceeds account balance
    def transfer(self, amount, recipient_account):
        if amount > self.balance: 
            print("Insufficient funds.")
        else:# code below shows the procedure of the withdrawing the amount from the current account, transfering amount in to recipient's account and generating transfer reciept
            self.withdraw(amount) 
            recipient_account.deposit(amount) 
            print(f"Transferred Ngultrum{amount} to account {recipient_account.account_number}")

    # process to change account number
    def change_account_number(self, new_account_number):
        self.account_number = new_account_number # account number is being updated

    # process to change password
    def change_password(self, new_password):
        self.password = new_password # password is being updated
#Account inheriting from Business account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0, business_name=""):
        super().__init__(account_number, password, "Business", balance)
        self.business_name = business_name
      # above codes is mainly to initialize the account base class and the bussiness name 

# account inherting from personal account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0, owner_name=""):
        super().__init__(account_number, password, "Personal", balance) 
        self.owner_name = owner_name  
    #the base account class and acoount holding were being initialized in the above code lines

#  Accounts is being save to a file by using following function
def save_account(account):
    accounts = load_accounts() #  load the file with the current accounts.
    accounts[account.account_number] = account #Make changes to or add the account.
    with open('accounts.txt', 'w') as f: #account file is being opened in write mode 
        for acc in accounts.values():# Iterating through all accounts using for loop
            f.write(f"{acc.account_number},{acc.password},{acc.account_type},Ngultrum {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  #account details is being written or save in the file 

# Function to load accounts from a file
def load_accounts():
    accounts = {}  # The empty dictionary is being initialized to store accounts
    if os.path.exists('accounts.txt'):  # checking the account file whether it exist or not 
        with open('accounts.txt', 'r') as f: # account file is open in read mode 
            for line in f: # every line contain in the file is being iterated
                parts = line.strip().split(',')  # line is said to be splitted
                account_number, password, account_type, balance = parts[:4]  # obtaining account information
                balance = float(balance.split()[1]) # After deleting the prefix "Ngultrum," returning the account balance to float 
                if account_type == "Business":  # checkin the account type whether it is for bussiness or not 
                    business_name = parts[4] # obtaining or retrieving business name
                    accounts[account_number] = BusinessAccount(account_number, password, balance, business_name) # Creating BusinessAccount object
                elif account_type == "Personal":  # verifying  the account type whether it is for personal or not with eving owerners name 
                    owner_name = parts[5] #obtaining owner's name
                    accounts[account_number] = PersonalAccount(account_number, password, balance, owner_name)  # Creating PersonalAccount object
    return accounts # getting back the  accounts dictionary

# Function to create or register new account
def create_account():
    account_number = str(random.randint(100000000, 999999999))#A random nine-digit account number is generated.
    password = str(random.randint(1000, 9999)) # creating a 4-digit password at randomly
    account_type = input("Enter account type (Business/Personal): ")# Prompt user to enter account type
    
    if account_type == "Business":  # checkingif account type is for business or not
        business_name = input("Enter business name: ")  # codes is maiinly to Ask user to provide the name of their businness. 
        account = BusinessAccount(account_number, password, business_name=business_name)# Making an item for a business account
    else: #if the type of account is personal
        owner_name = input("Enter holder name: ") # ask the  user to enter account owner's name 
        account = PersonalAccount(account_number, password, owner_name=owner_name)  # personal acount oject is being created by using this code

    save_account(account) # to save the new account to file
    print(f"Account created! Your account number is {account_number} and password is {password}")  # generating  account creation receipt

# Function to login to an account
def login(accounts):
    account_number = input("Enter account number: ") #prompt user to enter account number 
    password = input("Enter password: ") #asking user to enter account password
    
    account = accounts.get(account_number)  # acount is obtained from the account dictionary by using this code
    if account and account.password == password: # account verification and correctness of the password is being checked here 
        print(f"Welcome, {account.account_type} account holder!") # welcome message is printed here
        return account  #the logged-in account being returned
    else: # if the password supplied is invalid or if the account does not exist
        print("Invalid account number or password.") #  invalid login is printed as error message
        return None # None is returned for invalid login

# Function for the  account deletion
def delete_account(account):
    accounts = load_accounts() # to import current accounts from the file
    if account.account_number in accounts:  # checking the account exitance
        del accounts[account.account_number] # To delete the account from dictionary
        with open('accounts.txt', 'w') as f: # accounts file is open write mode
            for acc in accounts.values(): # going over each of the remaining accounts again
                f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file
        print("Account deleted successfully.")  # account deletion receipt is generated here
    else:
        print("Account not found.")

# acount details is change by using following fuctions
def change_account_details(account):
    print("\n1. Change Account Number\n2. Change Password") #creating alternatives to modify the account information
    choice = input("Enter choice: ") #ask user to enter their option
    
    if choice == '1': # acount numbers is being changed by using the following functions 
        new_account_number = input("Enter new account number: ") #asking user to enter new account number 
        accounts = load_accounts() # to import current accounts from the file
        if new_account_number in accounts: # checking the pre exitance of the new account number
            print("Account number already exists.") #if the account number is already in use or exist
        else:
            old_account_number = account.account_number  # to keep the previous account number save
            account.change_account_number(new_account_number) # to switch or change user(account numbers)
            save_account(account) # keeping a savings account with a new  acount number
            # To delete or remove the  old account
            if old_account_number in accounts:
                del accounts[old_account_number] # to delete or remove the  previous account from the dictionary
                with open('accounts.txt', 'w') as f:  #  accounts file is open in the write mode
                    for acc in accounts.values(): # Going over the remaining accounts one by one or it iterates
                        f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # account details is writing in the file
            print("Account number changed successfully.") # confiramtion message is said to be printed here
    elif choice == '2': #  to modify account password
        new_password = input("Enter new password: ") #asking the user to enter new password
        account.change_password(new_password) 
        save_account(account) # account is saving with new password
        print("Password changed successfully.") # confirmation message is printed here
    else:
        print("Invalid choice.")

# Main function
def main():
    while True: #infinite loop
        print("\n1. Create Account\n2. Login\n3. Exit") # Generating or creating choice
        choice = input("Enter choice: ") #asking user to enter their choice or option 
        
        if choice == '1': # to register or create account 
            create_account() # calling the function to create_account
        elif choice == '2': # for login
            accounts = load_accounts()  # existing accounts is being loaded by this code
            account = login(accounts)  #for the logging in
            if account: # checking whether the login was successful or not
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout") # Printing options or choice
                    trans_choice = input("Enter choice: ") #prompt user to enter their choice 
                    
                    if trans_choice == '1': # to deposit the amount
                        amount = float(input("Enter amount to deposit: ")) #asking the user to enter the  deposit amount 
                        account.deposit(amount) #  amount is depositing
                        save_account(account)# updated account details is said to be saved by this code
                    elif trans_choice == '2': #for withdraw purposes
                        amount = float(input("Enter amount to withdraw: "))#asking  the user to enter the amount for withdraw
                        account.withdraw(amount) # withdrawing amount
                        save_account(account)# Saving updated account details
                    elif trans_choice == '3': #checking account balance 
                        print(f"Balance: Ngultrum {account.check_balance()}") # current balance is  printed here
                    elif trans_choice == '4': #for the amount transference 
                        recipient_number = input("Enter recipient account number: ") #asking  the user to enter the account number of  recipent
                        recipient = accounts.get(recipient_number)  
                        if recipient: # verifying if recipient account exists
                            amount = float(input("Enter amount to transfer: ")) # above codes verifys reciepients account existance, asking the user to enter the transfer amount
                            account.transfer(amount, recipient)  #transfering amount 
                            save_account(account) 
                            save_account(recipient) 
                            # above codes save the sendesrs updated account details and reciepients updated account details
                        else:
                            print("Recipient account does not exist.")
                    elif trans_choice == '5': #for account deletion
                        delete_account(account)
                        break 
                    elif trans_choice == '6':#to modify account details 
                        change_account_details(account)
                    elif trans_choice == '7': # for logout 
                        save_account(account) #  account details is saving
                        print("Logged out.")
                        break #loop exits here
        elif choice == '3': # for program exist
            print("Thank You!")
            break # loop exist
        else:
            print("Invalid choice. Try again.")

#  Ensures that when the script is performed, the main function is called.
if __name__ == "__main__":
    main() #calling main function
    
    
