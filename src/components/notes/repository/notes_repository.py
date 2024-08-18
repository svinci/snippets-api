from src.components.notes.notes_model import Note

from abc import ABC, abstractmethod

NOTES_REPOSITORY_NAME='notes_repository'


class NotesRepository(ABC):

    @abstractmethod
    def get_all(self, user_id: str) -> list[Note]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str, note_id: str) -> Note | None:
        pass

    @abstractmethod
    def create(self, note: Note) -> None:
        pass

    @abstractmethod
    def update(self, note: Note) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, user_id: str, note_id: str) -> None:
        pass
