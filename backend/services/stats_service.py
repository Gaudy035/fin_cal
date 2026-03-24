from sqlalchemy.orm import Session
import models
from sqlalchemy import func

def get_stats(current_user:models.UzytkownikDB, db:Session):
    stats = db.query(models.KategoriaDB.nazwa.label("nazwa_kat"), func.sum(models.TransakcjaDB.kwota).label('total')).join(models.TransakcjaDB, models.KategoriaDB.id_kategorii==models.TransakcjaDB.id_kategorii).filter(models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika, models.TransakcjaDB.typ=='wydatek').group_by(models.KategoriaDB.nazwa).all()
    return [{"kategoria":stat.nazwa_kat,'kwota':stat.total} for stat in stats]

def get_summary(current_user:models.UzytkownikDB, db:Session ):
    summary = db.query(models.TransakcjaDB.typ, func.sum(models.TransakcjaDB.kwota).label('kwota')).filter(models.UzytkownikDB.id_uzytkownika==current_user.id_uzytkownika).group_by(models.TransakcjaDB.typ).all()
    return [{"typ":s.typ,"kwota":s.kwota} for s in summary]