from typing import Any, Dict

from Pack.Structure.Bank import BankAccount


class PersonMeta(type):
    def __new__(cls, name: str, bases: tuple[Any, ...], attrs: dict[str, Any]):
        attrs["__slots__"] = (
            "__full_name",
            "__age",
            "__cpf",
            "__rg",
            "__mom",
            "__dad",
            "__bank_account",
        )

        required_attrs = ["get_full_name", "set_full_name"]

        for attr in required_attrs:
            if attr not in attrs:
                raise AttributeError(f"Missing required attribute {attr}")

        return super().__new__(cls, name, bases, attrs)


class Person(metaclass=PersonMeta):
    def __init__(
        self,
        full_name: str,
        age: int,
        cpf: str,
        rg: str,
        mom: str,
        bank_account: BankAccount | None | Dict[Any, Any] = None,
        dad: str | None = None,
    ) -> None:
        self.__full_name = full_name
        self.__age = age
        self.__cpf = cpf
        self.__rg = rg
        self.__mom = mom
        self.__dad = dad
        self.__bank_account = bank_account

    def get_bank_account(self) -> BankAccount | Dict[Any, Any]:
        if self.__bank_account:
            return self.__bank_account
        else:
            return BankAccount("None", None, 1)

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

    def get_dad(self) -> str | None:
        return self.__dad

    def set_bank_account(self, account: BankAccount) -> None:
        if self.__bank_account is None:
            self.__bank_account = account
        else:
            print(f"{self.__full_name} already has an account")

    def set_full_name(self, full_name: str) -> None:
        self.__full_name = full_name

    def set_age(self, age: int) -> None:
        self.__age = age

    def set_cpf(self, cpf: str) -> None:
        self.__cpf = cpf

    def set_rg(self, rg: str) -> None:
        self.__rg = rg

    def set_mom(self, mom: str) -> None:
        self.__mom = mom

    def set_dad(self, dad: str | None) -> None:
        self.__dad = dad

    def __str__(self) -> str:
        final = {
            "name": self.__full_name,
            "age": self.__age,
            "cpf": self.__cpf,
            "rg": self.__rg,
            "mother": self.__mom,
            "father": self.__dad,
            "bank_account": self.__bank_account,
        }

        return f"{final}"
