from src.infrastructure.storage.file import ensure_file_exists
from dataclasses import dataclass
import json


@dataclass
class JSONRepository:
    file_directory: str
    file_name: str

    delimiter: str = ','

    def read(self) -> dict:
        ensure_file_exists(self.file_directory, self.file_name)

        with open(f'{self.file_directory}/{self.file_name}', 'r') as f:
            return json.load(f)
    
    def write(self, data: dict) -> None:
        ensure_file_exists(self.file_directory, self.file_name)

        with open(f'{self.file_directory}/{self.file_name}', 'w') as f:
            json.dump(data, f)
