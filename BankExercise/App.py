import os
from Pack.Structure.Bank import Bank,BankAccount,AccountType
from Pack.Structure.Person import Person
from Pack.Structure.DataBase import PWDB, USDB

'== == == == == == == global section == == == == == == =='

wise_bank = Bank(
        name="Wise",
        location="Belgium",
        id_code="01123-1"
        )

revolut_bank = Bank(
        name="Revolut",
        location="Belgium",
        id_code="01313-1"
        )

wise_account = BankAccount(
        account_type = AccountType(1),
        bank_holder = wise_bank,
        level=3
        )

revolut_account = BankAccount(
        account_type = AccountType(2),
        bank_holder = revolut_bank,
        level=2
        )


'== == == == == == == function section == == == == == == =='

def create_user_and_pwd(db:PWDB, user:Person):
    '''
    Get the username and password. Requirements:
    - Username must be unique in the password DB
    - Password must be at least 8 characters and contain at least one non-alphanumeric character
    '''
    while True:
        username = input("username: ")
        # Check username uniqueness
        username_taken = False
        for record in db.read_records():
            if record.get("username") == username:
                username_taken = True
                break
        if username_taken:
            print("Username already exists. Please choose another.")
            continue

        password = input("password: ")
        confirm_pass = input("confirm password: ")

        # Password requirements
        if len(password) < 8 or password.isalnum():
            print("Password must be at least 8 characters and contain at least one special character.")
            continue

        if password != confirm_pass:
            print("Passwords do not match.")
            continue

        try:
            db.create_record_pwd(username=username, password=password, new_record=user)
            print("User and password created successfully.")
            break
        except ValueError:
            print("Error creating user and password. Try again.")


def add_user(db:PWDB|USDB, user:Person) -> bool:
    '''Check if user is not on the file. If not, create the user.'''
    user_exists, _ = db.read_record_by_user(user)
    if user_exists:
        print("User Already Exists")
        return True
    else:
        db.create_record(user)
        print("User Added Successfully")
        return False


def create_bank_account() -> BankAccount|None:
    bank_opt = input("[1 - Wise]\n[2 - Revolut]\n> ")
    try:
        if int(bank_opt) == 1:
            return BankAccount(
                    AccountType(1),
                    bank_holder=wise_bank,
                    level=2
                    )

        elif int(bank_opt) == 2:
            return BankAccount(
                    account_type=AccountType(1),
                    bank_holder=revolut_bank,
                    level=2,
                    )

        else:
            raise ValueError
    
    except ValueError:
        if bank_opt.lower() == "wise":
            return BankAccount(
                    AccountType(1),
                    bank_holder=wise_bank,
                    level=2
                    )

        elif bank_opt.lower() == "revolut":
            return BankAccount(
                    AccountType(1),
                    bank_holder=revolut_bank,
                    level=2
                    )
        else:
            print("number not valid")

        print("Number not Valid")



def get_user_info() -> Person:
    name = input("Your Full Name: ")
    age = int(input("Your Age: "))
    mom = input("Your Mother: ")
    father = input("Your Father: ")
    cpf = input("CPF: ")
    rg = input("RG: ")

    print("Do you wish to create a bank account? ")
    create_account = input("> ")


    if create_account.lower() == ("yes" or "ye" or "y"):
        bank_account = create_bank_account()
        return Person(full_name=name,age=age,mom=mom,dad=father, cpf=cpf, rg=rg, bank_account=bank_account)

    elif create_account.lower() == ("no" or "n"):
        return Person(full_name=name, age=age, mom=mom, dad=father, cpf=cpf, rg=rg)

    else:
        return Person(full_name=name, age=age, mom=mom, dad=father, cpf=cpf, rg=rg)


def create_database()-> list[USDB|PWDB]:

    want_2_databases = input("Would you like to split the database ? ")

    if str(want_2_databases).lower() == ("yes" or "y"):
        user_db_name = str(input("Name for the folder of users "))
        pass_db_name = str(input("Name for the folder of passw "))

    elif str(want_2_databases.lower()) == ("no" or "n"):
        user_db_name = "UserData"
        pass_db_name = "PassData"

    else:
        os.system("clear")
        print("Database not set properly\ndefault db is UserData and PassData on the app folder\n\n")
        user_db_name = "UserData"
        pass_db_name = "PassData"

    user_db = USDB(user_db_name)
    pass_db = PWDB(pass_db_name)

    return [user_db, pass_db]



def user_register():
    '''
    get basic info, such as full name, age, cpf, rg,mom,dad,bank_account
    '''
    user_db, pass_db = create_database()
    person = get_user_info()
    return [user_db,pass_db, person]

def main():
    user_db, pass_db, person = user_register()

    # Add user to user_db if not exists
    add_user(db=user_db, user=person)

    print("Wanna create a user and password?")
    value = input("[ yes ]|[ no ]> ")

    # Always check/add user to pass_db as well
    passdb_user_exists, _ = pass_db.read_record_by_user(person)

    if value.lower() == 'yes':
        print("Creating user and password in password database...")
        if not passdb_user_exists:
            create_user_and_pwd(pass_db, person)
        else:
            print("User already exists in password database.")
    else:
        print("Login...")
        print("\n" * 10)
        username = input("username: ")
        password = input("password: ")

        # Check if the username and password match the one from the db
        if pass_db.login_user_pwd(person, username, password):
            print("Login successful!")
            # Proceed with the application
        else:
            print("Login failed. Invalid username or password.")


if __name__ == "__main__":
    main()
