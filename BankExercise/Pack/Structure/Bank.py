from copy import Error
from typing import Any


class MetaBank(type):
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        return super().__new__(cls, name, bases, attrs)


class Bank(metaclass=MetaBank):
    def __init__(self, name: str, location: str, id_code: int | str) -> None:
        self.__location = location
        self.__id = id_code
        self.__name = name

    def get_id_code(self) -> str:
        return f"Bank Id: {self.__id}"

    def set_id_code(self, id_code: str | int) -> None:
        self.__id = f"{id_code}"

    def get_location(self) -> str:
        return f"Bank place: {self.__location}"

    def set_location(self, location: str) -> None:
        self.__location = location

    def get_name(self) -> str:
        return f"Bank name: {self.__name}"

    def set_name(self, name: str) -> None:
        self.__name = name

    def __str__(self) -> str:
        return f"Bank info: {self.__name}, {self.__id}, {self.__location}"


class AccountType:
    def __init__(self, account_choice: int | None) -> None:
        self.__account_type = {
            1: "Savings Account",
            2: "Current Account",
            3: "Special Account",
        }

        if (account_choice is not None) and (account_choice in self.__account_type):
            self.__account = self.__account_type[account_choice]
        else:
            raise Error("Error chosing the account type")

    def get_account_type(self):
        return f"{self.__account}"

    def __str__(self) -> str:
        return f"{self.__account}"

    """
    CORRENTE E POUPANCA, CORRENTE(DEBITO, CREDITO), POUPANCA(DEBITO) RETORNA UM REDIMENTO (110% CDI)
    """


class BankAccount:
    def __init__(
        self,
        account_type: AccountType,
        bank_holder: Bank | None,
        level: int = 0,
        balance: float | int = 0,
    ) -> None:
        self.__account_type: AccountType | str = account_type
        self.__bank_holder: Bank | None = bank_holder
        self.__level: int | None = level
        self.__balance = balance

    def get_account_type(self) -> AccountType:
        return self.__account_type if not isinstance(self.__account_type, str)

    def set_account_type(self, account: AccountType) -> None:
        self.__account_type = account

    def get_balance(self) -> float | int:
        return self.__balance

    def set_balance(self, balance: int | float) -> None:
        self.__balance = balance if balance > 0 else self.__balance

    def get_bank_holder(self) -> Bank | None:
        return self.__bank_holder

    def set_bank_holder(self, bank_holder: Bank) -> None:
        self.__bank_holder = bank_holder

    def get_level(self) -> int | None:
        return self.__level

    def set_level(self, level: int) -> None:
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
