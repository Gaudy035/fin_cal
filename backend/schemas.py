from pydantic import BaseModel, ConfigDict
from datetime import date, timedelta

# region uzytkownik

class UzytkownikBase(BaseModel):
    imie:str
    nazwisko:str
    email:str

class UzytkownikCreate(UzytkownikBase):
    haslo:str

class UzytkownikResponse(UzytkownikBase):
    id_uzytkownika:int
    czy_aktywny:bool | None
    model_config = ConfigDict(from_attributes=True)

class EmailChange(BaseModel):
    current_pass:str
    new_email:str

class PasswordChange(BaseModel):
    current_pass:str
    new_pass:str

# endregion uzytkownik

class Kategoria(BaseModel):
    id_kategorii:int
    nazwa:str
    model_config = ConfigDict(from_attributes=True)

# region transakcja

class TransakcjaBase(BaseModel):
    id_uzytkownika:int | None = None
    id_kategorii:int | None = None
    typ:str
    tytul:str
    opis:str | None = None
    kwota:float
    metoda:str
    konto:str | None = None
    wlasciciel_konta:str | None = None

class TransakcjaCreate(TransakcjaBase):
    data:date | None = None

class TransakcjaResponse(TransakcjaBase):
    id_transakcji:int
    data:date
    model_config = ConfigDict(from_attributes=True)
    
# endregion transakcja

# region powtarzalne

class PowtarzalnaBase(TransakcjaBase):
    co_ile:timedelta
    nastepny_termin:date

class PowtarzalnaCreate(PowtarzalnaBase):
    pass
    
class PowtarzalnaResponse(PowtarzalnaBase):
    id_t_powtarzalnej:int
    czy_aktywna:bool
    model_config = ConfigDict(from_attributes=True)

# endregion powtarzalne