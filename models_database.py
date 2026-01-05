from pydantic import BaseModel, ValidationError, Field

class Occorrenza(BaseModel):
    parola:     str = Field(default="")
    testo:      str = Field(default="")

class UtenteOccorrenze(BaseModel):
    nome:       str = Field(default="")
    occorrenze: list[Occorrenza]

class BodyUtenti(BaseModel):
    utenti:     list[UtenteOccorrenze]

class Universita(BaseModel):
    nome:       str = Field(default="")
    corso:      str = Field(default="")
    voto:       str = Field(default="")

class UtenteUniversita(BaseModel):
    nome:       str = Field(default="")
    universita: list[Universita]

class BodyUtenteUniversita(BaseModel):
    utenti:     list[UtenteUniversita] 