from src.components.notes.repository.notes_repository import NotesRepository, NOTES_REPOSITORY_NAME
from src.components.notes.notes_model import Note
from src.infrastructure.storage.json_repository import JSONRepository
from src.infrastructure.storage.file import file_exists, remove_file, get_files_in_directory
from src.infrastructure.dataclasses import from_dict, to_dict

from beenchee.peanut import peanut

@peanut(
    name=NOTES_REPOSITORY_NAME,
    configs={
        'storage_folder': 'storage_folder'
    }
)
class NotesFileSystemRepository(NotesRepository):
    storage_folder: str
    
    def get_all(self, user_id: str) -> list[Note]:
        notes_files = self._get_notes_directory(user_id)
        notes_ids = [file.split('.')[0] for file in get_files_in_directory(notes_files)]
        return [self.get_by_id(user_id, note_id) for note_id in notes_ids]

    def get_by_id(self, user_id: str, note_id: str) -> Note | None:
        if not self._exists(user_id, note_id):
            return None
        
        note_dict = self._get_json_repository(user_id, note_id).read()
        return from_dict(Note, note_dict)

    def create(self, note: Note) -> None:
        self._get_json_repository(note.user_id, note.id).write(to_dict(note))

    def update(self, note: Note) -> None:
        self.create(note)

    def delete_by_id(self, user_id: str, note_id: str) -> None:
        remove_file(
            directory_path=self._get_notes_directory(user_id),
            file_name=self._get_note_file_name(note_id)
        )

    def _exists(self, user_id: str, note_id: str) -> bool:
        return file_exists(
            directory_path=self._get_notes_directory(user_id),
            file_name=self._get_note_file_name(note_id)
        )

    def _get_json_repository(self, user_id: str, note_id: str) -> JSONRepository:
        return JSONRepository(
            file_directory=self._get_notes_directory(user_id),
            file_name=self._get_note_file_name(note_id)
        )
    
    def _get_notes_directory(self, user_id: str) -> str:
        return f'{self.storage_folder}/{user_id}'
    
    def _get_note_file_name(self, note_id: str) -> str:
        return f'{note_id}.json'
