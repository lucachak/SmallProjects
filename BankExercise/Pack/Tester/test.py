from typing import Any
from copy import Error
class MetaBank(type):
    def __new__(cls, name:str, bases:tuple[type,...], attrs:dict[str, Any]):
        return super().__new__(cls, name, bases, attrs)

class Bank(metaclass=MetaBank):

    def __init__(self, name:str, location:str, id_code:int|str ) -> None:
        self.__location = location
        self.__id = id_code
        self.__name = name


    def get_id_code(self)->str:
        return f"Bank Id: {self.__id}"

    def set_id_code(self, id_code:str|int)->None:
        self.__id =  f"{id_code}"

    def get_location(self)->str:
        return f"Bank place: {self.__location}"

    def set_location(self, location:str)->None:
        self.__location = location

    def get_name(self)->str:
        return f"Bank name: {self.__name}"

    def set_name(self, name:str)->None:
        self.__name = name


    def __str__(self) ->str:
        return f"Bank info: {self.__name}, {self.__id}, {self.__location}"


class AccountType:

    def __init__(self,account_choice:int|None) -> None:
        self.__account_type = {
            1: "Savings Account",
            2: "Current Account",
            3: "Special Account"
        }

        if (account_choice != None) and (account_choice in self.__account_type):
            self.__account = self.__account_type[account_choice]
        else:
            raise Error("Error chosing the account type")


    def get_account_type(self)->str:
        return f"{self.__account}"

    def __str__(self)->str:
        return f"{self.__account}"

    '''
    CORRENTE E POUPANCA, CORRENTE(DEBITO, CREDITO), POUPANCA(DEBITO) RETORNA UM REDIMENTO (110% CDI)
    '''


class BankAccount:

    def __init__(self,
                 account_type:AccountType|str,
                 bank_holder:Bank,
                 level:int=0,
                 ) -> None:

        self.__account_type:AccountType|str = account_type
        self.__bank_holder:Bank = bank_holder
        self.__level:int|None = level
        self.__balance = 0

    def get_account_type(self)->AccountType|str:
        return self.__account_type
    def set_account_type(self, account:AccountType|str)->AccountType|None:
        self.__account_type = account

    def get_balance(self) -> float|int:
        return self.__balance
    def set_balance(self, balance:int|float) -> None:
        self.__balance = balance if balance > 0 else self.__balance

    def get_bank_holder(self)->Bank:
        return self.__bank_holder
    def set_bank_holder(self, bank_holder:Bank)->None:
        self.__bank_holder = bank_holder

    def get_level(self)->int|None:
        return self.__level
    def set_level(self, level:int)->None:
        self.__level = level

    def __str__(self) -> str:
        if self.__level == 3:
            return f"Adult type:{self.__account_type} level:{self.__level}\n{self.__bank_holder}\n"
        elif self.__level == 2:
            return f"Student type:{self.__account_type} level:{self.__level}\n{self.__bank_holder}\n"
        elif self.__level == 1:
            return f"Child type:{self.__account_type} level:{self.__level}\n{self.__bank_holder}\n"
        else:
            return f"{self.__level} not identified"


class PersonMeta(type):
    def __new__(cls, name:str, bases:tuple[Any,...], attrs:dict[str, Any]):
        attrs['__slots__'] = ('__full_name', '__age', '__cpf', '__rg', '__mom', '__dad', '__bank_account')

        required_attrs = ['get_full_name', 'set_full_name']

        for attr in required_attrs:
            if attr not in attrs:
                raise AttributeError(f"Missing required attribute {attr}")

        return super().__new__(cls, name, bases, attrs)


class Person(metaclass=PersonMeta):

    def __init__(self,
                 full_name:str,
                 age:int,
                 cpf:str,
                 rg:str,
                 mom:str,
                 bank_account:BankAccount|None=None,
                 dad:str|None=None,
                 ) -> None:


        self.__full_name = full_name
        self.__age = age
        self.__cpf = cpf
        self.__rg = rg
        self.__mom = mom
        self.__dad = dad
        self.__bank_account = bank_account


    def get_bank_account(self)->BankAccount|None:
        if self.__bank_account:
            return self.__bank_account
        else:
            return None

    def get_full_name(self) -> str:
        return self.__full_name

    def get_age(self) -> int:
        return self.__age

    def get_cpf(self) -> str:
        return self.__cpf

    def get_rg(self) -> str:
        return self.__rg

    def get_mom(self) -> str:
        return self.__mom

    def get_dad(self) -> str|None:
        return self.__dad



    def set_bank_account(self, account:BankAccount)->None:
        if self.__bank_account == None:
            self.__bank_account = account
        else:
            print(f"{self.__full_name} already has an account")

    def set_full_name(self, full_name:str) -> None:
        self.__full_name = full_name

    def set_age(self, age:int) -> None:
        self.__age = age

    def set_cpf(self, cpf:str) -> None:
        self.__cpf = cpf

    def set_rg(self, rg:str) -> None:
        self.__rg = rg

    def set_mom(self, mom:str) -> None:
        self.__mom = mom

    def set_dad(self, dad:str|None) -> None:
        self.__dad = dad

    def __str__(self) -> str:

        final = {
            'name':self.__full_name,
            'age':self.__age,
            'cpf':self.__cpf,
            'rg':self.__rg,
            'mother':self.__mom,
            'father':self.__dad,
            'bank_account':self.__bank_account
        }

        return f'{final}'


person = [
    {
        "id": 1,
        "full_name": "lucas almeida lucachak amorin",
        "age": 23,
        "cpf": "455.724.128-05",
        "rg": "38.045.894-12",
        "mother": "Gracione Gome da Silva",
        "father": "Rogerio Lucachak Amorin",
        "bank_account": {
            "account_type": "Savings Account",
            "bank_holder": "Bank info: Wise, 01123-1, Belgium",
            "level": 2,
            "balance": 0.0
        },
        "username": "LucachakLucas",
        "password": "Lucachaklucas"
    }
]


def main():


    if person[0]['bank_account']:
        user = Person(
            full_name=str(person[0]["full_name"]),
            age=int(str(person[0]["age"])),
            cpf=str(person[0]["cpf"]),
            rg=str(person[0]["rg"]),
            mom=str(person[0]["mother"]),
            dad=str(person[0]["father"]),
            bank_account=BankAccount(
                    account_type=str(person[0]['bank_account']['account_type']),
                    bank_holder=str(person[0]['bank_account']['bank_holder']),
                    level=int(person[0]['bank_account']['level']),
                    balance=float(person[0]['bank_account']['balance'])
            )
        )
    else:
        user = Person(
            full_name=str(person[0]["full_name"]),
            age=int(str(person[0]["age"])),
            cpf=str(person[0]["cpf"]),
            rg=str(person[0]["rg"]),
            mom=str(person[0]["mother"]),
            dad=str(person[0]["father"]),
        )
    print(user.get_full_name())

if __name__ == "__main__":
    main()
