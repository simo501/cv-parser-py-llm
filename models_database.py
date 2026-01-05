from pydantic import BaseModel, ValidationError

class Occorrenza(BaseModel):
    parola:     str
    testo:      str

class Utente(BaseModel):
    nome:       str
    occorrenze: list[Occorrenza]

class Body(BaseModel):
    utenti: list[Utente]