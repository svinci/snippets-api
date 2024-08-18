from src.infrastructure.storage.file import ensure_file_exists, file_exists
from dataclasses import dataclass
from csv import DictReader, DictWriter


@dataclass
class CSVRepository:
    file_directory: str
    file_name: str

    delimiter: str = ','

    def read(self) -> list[dict]:
        ensure_file_exists(self.file_directory, self.file_name)

        with open(f'{self.file_directory}/{self.file_name}', 'r') as f:
            reader = DictReader(f, delimiter=self.delimiter)
            return [row for row in reader]
    
    def write(self, data: list[dict]) -> None:
        if file_exists(self.file_directory, self.file_name):
            self._append(data)
        else:
            self._write(data)
    
    def _append(self, data: list[dict]) -> None:
        ensure_file_exists(self.file_directory, self.file_name)

        with open(f'{self.file_directory}/{self.file_name}', 'a') as f:
            writer = DictWriter(f, fieldnames=data[0].keys(), delimiter=self.delimiter)
            writer.writerows(data)

    def _write(self, data: list[dict]) -> None:
        ensure_file_exists(self.file_directory, self.file_name)

        with open(f'{self.file_directory}/{self.file_name}', 'w') as f:
            writer = DictWriter(f, fieldnames=data[0].keys(), delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(data)
