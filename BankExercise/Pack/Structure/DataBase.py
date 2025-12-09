import json
import os
from functools import cache
from typing import Any, Dict, List, Optional

from Pack.Structure.Person import Person  # Ensure this import path is correct


class DataBase:
    def __init__(self, path: Optional[str] = None, file: str = "data.json"):
        """Initialize the database with optional path and filename.
        Args:
            path: Directory path (created if doesn't exist)
            file: JSON filename
        """
        self._file = os.path.join(path, file) if path and file else file
        self._ensure_directory_exists()
        self._setup_base()

    def _ensure_directory_exists(self):
        """Create parent directory if it doesn't exist."""
        dir_path = os.path.dirname(self._file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def _setup_base(self):
        """Initialize JSON file with empty list if it doesn't exist."""
        if not os.path.exists(self._file):
            with open(self._file, "w") as f:
                json.dump([], f)

    def _encoder(self, obj: Person) -> Dict[str, Any]:
        """Convert Person object to serializable dictionary.
        Args:
            obj: Person instance
        Returns:
            Dictionary representation
        Raises:
            TypeError: If obj isn't a Person
        """

        if not isinstance(obj, Person):
            raise TypeError("Object must be a Person instance")

        bankAccount = obj.get_bank_account()

        return {
            "id": getattr(obj, "id", None),  # Handle missing ID
            "full_name": obj.get_full_name(),
            "age": obj.get_age(),
            "cpf": obj.get_cpf(),
            "rg": obj.get_rg(),
            "mother": obj.get_mom(),
            "father": obj.get_dad(),
            "bank_account": {
                "account_type": f"{bankAccount.get_account_type()}",
                "bank_holder": f"{bankAccount.get_bank_holder()}",
                "level": int(f"{bankAccount.get_level()}"),
                "balance": float(f"{bankAccount.get_balance()}"),
            }
            if bankAccount is not None
            else None,
        }

    def _decoder(self, index: int) -> Person:
        """Convert dictionary record back to Person object.
        Args:
            index: Record index/ID
        Returns:
            Person instance
        """
        person_data = self.read_record(index)

        # Extract bank account data if it exists
        bank_account_data = None
        if person_data.get("bank_account"):
            bank_account_data = {
                "account_type": str(person_data["bank_account"]["account_type"]),
                "bank_holder": str(person_data["bank_account"]["bank_holder"]),
                "level": int(person_data["bank_account"]["level"]),
                "balance": float(person_data["bank_account"]["balance"]),
            }

        return Person(
            full_name=str(person_data["full_name"]),
            age=int(str(person_data["age"])),
            cpf=str(person_data["cpf"]),
            rg=str(person_data["rg"]),
            mom=str(person_data["mother"]),
            dad=str(person_data["father"]),
            bank_account=bank_account_data,
        )

    def read_records(self) -> List[Dict[str, Any]]:
        """Read all records from JSON file.
        Returns:
            List of records (empty list if file is empty/corrupt)
        """
        try:
            with open(self._file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @cache
    def read_record_by_user(self, user: Person):
        values = self.read_records()

        for i in range(len(values)):
            if user.get_full_name() == values[i]["full_name"]:
                print(f"user id is: {values[i]['id']}")
                return [True, values[i]]
        return [False, values]

    def read_record(self, record_id: int) -> Dict[str, Any]:
        """Get specific record by ID.
        Args:
            record_id: Integer ID to search for
        Returns:
            Record dictionary
        Raises:
            ValueError: If record not found
        """
        records = self.read_records()
        for record in records:
            if record.get("id") == record_id:
                return record
        raise ValueError(f"Record with ID {record_id} not found")

    def create_record(self, new_record: Person) -> Dict[str, Any]:
        """Add new record to database.
        Args:
            new_record: Person instance to add
        Returns:
            Created record with generated ID
        """
        records = self.read_records()
        record_data = self._encoder(new_record)

        # Generate sequential ID
        record_data["id"] = max((r["id"] for r in records), default=0) + 1

        records.append(record_data)
        self._save_records(records)
        return record_data

    def update_record(
        self, record_id: int, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update existing record.
        Args:
            record_id: ID of record to update
            updated_data: Dictionary of fields to update
        Returns:
            Updated record
        Raises:
            ValueError: If record not found
        """
        records = self.read_records()
        updated = False

        for record in records:
            if record.get("id") == record_id:
                record.update(updated_data)
                updated = True
                break

        if not updated:
            raise ValueError(f"Record with ID {record_id} not found")

        self._save_records(records)
        return self.read_record(record_id)

    def delete_record(self, record_id: int) -> bool:
        """Remove record by ID.
        Args:
            record_id: ID of record to delete
        Returns:
            True if deleted
        Raises:
            ValueError: If record not found
        """
        records = self.read_records()
        initial_count = len(records)
        records = [r for r in records if r.get("id") != record_id]

        if len(records) == initial_count:
            raise ValueError(f"Record with ID {record_id} not found")

        self._save_records(records)
        return True

    def _save_records(self, records: List[Dict[str, Any]]):
        """Internal method to save records to file."""
        with open(self._file, "w") as f:
            json.dump(records, f, indent=4)

    def __repr__(self) -> str:
        return f"DataBase(file='{self._file}')"


class USDB(DataBase):
    def __init__(
        self,
        path: Optional[str] = None,
        file_name: str = "user_data.json",
        user: Optional[Person] = None,
    ):
        super().__init__(path, file_name)
        self._user = user  # Changed to protected attribute

    def __repr__(self) -> str:
        return f"USDB(file='{self._file}', user={self._user})"


class PWDB(DataBase):
    def __init__(
        self,
        path: Optional[str] = None,
        file_name: str = "pass_data.json",
        user: Optional[Person] = None,
    ):
        super().__init__(path, file_name)
        self._user = user  # Changed to protected attribute

    def create_record_pwd(
        self, username: str, password: str, new_record: Person
    ) -> Dict[str, Any]:
        records = self.read_records()
        record_data = self._encoder(new_record)
        record_data["id"] = max((r["id"] for r in records), default=0) + 1
        record_data["username"] = username
        record_data["password"] = password

        records.append(record_data)
        self._save_records(records)
        return record_data

    def login_user_pwd(self, person: Person, username: str, password: str) -> bool:
        records = self.read_records()
        for record in records:
            if (
                record.get("username") == username
                and record.get("password") == password
                and record.get("full_name") == person.get_full_name()
            ):
                return True
        return False

    def __repr__(self) -> str:
        return f"PWDB(file='{self._file}', user={self._user})"
