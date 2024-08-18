from src.components.notes.notes_service import NotesService, NOTES_SERVICE_NAME
from src.components.notes.notes_model import GetNoteRequest, GetNotesRequest, CreateNoteRequest, UpdateNoteRequest, DeleteNoteRequest
from src.infrastructure.dataclasses import to_dict
from src.infrastructure.model import APIError, Router, ROUTERS_TAG
from src.infrastructure.authenticated import authenticated
from src.infrastructure.flask.request_context import RequestContext, REQUEST_CONTEXT_NAME

from beenchee.peanut import peanut
from flask import Flask, request

NOTES_ROUTER_NAME='notes_router'


@peanut(
    name=NOTES_ROUTER_NAME,
    deps={
        'notes_service': NOTES_SERVICE_NAME,
        'request_context': REQUEST_CONTEXT_NAME,
    },
    tags=f'{ROUTERS_TAG}'
)
class NotesRouter(Router):
    notes_service: NotesService
    request_context: RequestContext

    def route(self, app: Flask) -> None:
        @app.route('/users/<user_id>/notes', methods=['GET'])
        @authenticated
        def get_all_notes(user_id: str):
            if user_id != self.request_context.get_user().id:
                raise APIError('Forbidden', 403)
            
            all_notes = self.notes_service.get_all(
                GetNotesRequest(
                    user_id=user_id, 
                    encryption_key=''
                )
            )

            return {
                'notes': [to_dict(note) for note in all_notes]
            }

        @app.route('/users/<user_id>/notes/<note_id>', methods=['GET'])
        @authenticated
        def get_note_by_id(user_id: str, note_id: str):
            if user_id != self.request_context.get_user().id:
                raise APIError('Forbidden', 403)
            
            note = self.notes_service.get_by_id(
                GetNoteRequest(
                    user_id=user_id, 
                    note_id=note_id, 
                    encryption_key=''
                )
            )

            if note is None:
                return {'message': 'Note not found'}, 404
            return to_dict(note)

        @app.route('/users/<user_id>/notes', methods=['POST'])
        @authenticated
        def create_note(user_id: str):
            if user_id != self.request_context.get_user().id:
                raise APIError('Forbidden', 403)
            
            name = request.json.get('name', '')
            content = request.json.get('content', '')

            note = self.notes_service.create(
                CreateNoteRequest(
                    user_id=user_id, 
                    name=name, 
                    content=content, 
                    encryption_key=''
                )
            )

            return to_dict(note)

        @app.route('/users/<user_id>/notes/<note_id>', methods=['PUT'])
        @authenticated
        def update_note(user_id: str, note_id: str):
            if user_id != self.request_context.get_user().id:
                raise APIError('Forbidden', 403)
            
            name = request.json.get('name', '')
            content = request.json.get('content', '')

            note = self.notes_service.update(
                UpdateNoteRequest(
                    user_id=user_id, 
                    note_id=note_id, 
                    name=name, 
                    content=content, 
                    encryption_key=''
                )
            )

            return to_dict(note)
        
        @app.route('/users/<user_id>/notes/<note_id>', methods=['DELETE'])
        @authenticated
        def delete_note(user_id: str, note_id: str):
            if user_id != self.request_context.get_user().id:
                raise APIError('Forbidden', 403)
            
            self.notes_service.delete(
                DeleteNoteRequest(
                    user_id=user_id, 
                    note_id=note_id, 
                    encryption_key=''
                )
            )

            return { 'message': 'ok' }, 200
