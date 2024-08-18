from src.components.notes.notes_model import Note, NoteSummary, GetNoteRequest, GetNotesRequest, CreateNoteRequest, UpdateNoteRequest, DeleteNoteRequest
from src.components.notes.repository import NotesRepository, NOTES_REPOSITORY_NAME
from src.infrastructure.model import APIError

from beenchee.peanut import peanut
from uuid import uuid4
import logging

NOTES_SERVICE_NAME = 'notes_service'
logger = logging.getLogger(__name__)


@peanut(
    name=NOTES_SERVICE_NAME,
    deps={
        'notes_repository': NOTES_REPOSITORY_NAME,
    }
)
class NotesService:
    notes_repository: NotesRepository

    def get_all(self, request: GetNotesRequest) -> list[NoteSummary]:
        notes = self.notes_repository.get_all(request.user_id)
        return [
            NoteSummary(
                id=note.id,
                user_id=note.user_id,
                name=note.name,
            )
            for note in notes
        ]
    
    def get_by_id(self, request: GetNoteRequest) -> Note | None:
        return self.notes_repository.get_by_id(request.user_id, request.note_id)

    def create(self, request: CreateNoteRequest) -> Note:
        if not request.name:
            raise APIError('Name is required', 400)
        if not request.content:
            raise APIError('Content is required', 400)

        note = Note(
            id=uuid4().__str__(),
            user_id=request.user_id,
            name=request.name,
            content=request.content,
        )
        self.notes_repository.create(note)

        return note

    def update(self, request: UpdateNoteRequest) -> Note:
        existing_note = self.notes_repository.get_by_id(request.user_id, request.note_id)
        if not existing_note:
            logger.info(f'Creating new note with fixed id {request.note_id}.')

        if not request.name:
            raise APIError('Name is required', 400)
        if not request.content:
            raise APIError('Content is required', 400)

        note = Note(
            id=request.note_id,
            user_id=request.user_id,
            name=request.name,
            content=request.content,
        )
        self.notes_repository.update(note)

        return note
    
    def delete(self, request: DeleteNoteRequest) -> None:
        self.notes_repository.delete_by_id(request.user_id, request.note_id)
