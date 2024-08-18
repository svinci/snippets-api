from dataclasses import dataclass


@dataclass
class Note:
    id: str
    user_id: str

    name: str
    content: str


@dataclass
class NoteSummary:
    id: str
    user_id: str

    name: str


@dataclass
class GetNotesRequest:
    user_id: str
    encryption_key: str

@dataclass
class GetNoteRequest(GetNotesRequest):
    note_id: str


@dataclass
class CreateNoteRequest(GetNotesRequest):
    name: str
    content: str


@dataclass
class UpdateNoteRequest(GetNotesRequest):
    note_id: str
    name: str
    content: str


DeleteNoteRequest = GetNoteRequest
