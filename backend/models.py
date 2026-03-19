from database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Numeric, Date, Text, ForeignKey, CheckConstraint, Interval
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class UzytkownikDB(Base):
    __tablename__ = "t_uzytkownik"

    id_uzytkownika = Column(Integer, primary_key=True, index=True, autoincrement=True)
    imie = Column(String(30), nullable=False)
    nazwisko = Column(String(30), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    haslo = Column(String(255), nullable=False)
    data_zalozenia = Column(TIMESTAMP, server_default=func.now())
    czy_aktywny = Column(Boolean, default=True)
    data_usuniecia = Column(TIMESTAMP, nullable=True)
    # relacje
    transakcje_fk = relationship("TransakcjaDB", back_populates="uzytkownik_fk")
    powtarzalne_fk = relationship("PowtarzalnaDB", back_populates="uzytkownik_fk")

class KategoriaDB(Base):
    __tablename__ = "t_kategorie"

    id_kategorii = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nazwa = Column(String(30), unique=True, nullable=False)
    # relacje
    transakcje_fk = relationship("TransakcjaDB", back_populates="kategoria_fk")
    powtarzalne_fk = relationship("PowtarzalnaDB", back_populates="kategoria_fk")

class TransakcjaDB(Base):
    __tablename__ = "t_transakcje"

    id_transakcji = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # klucze
    id_uzytkownika = Column(Integer, ForeignKey("t_uzytkownik.id_uzytkownika", ondelete="CASCADE"), nullable=False)
    id_kategorii = Column(Integer, ForeignKey("t_kategorie.id_kategorii", ondelete="CASCADE"))
    # kolumny
    typ = Column(String(10), nullable=False)
    tytul = Column(String(100), nullable=False)
    opis = Column(Text, nullable=True)
    kwota = Column(Numeric(12, 2), nullable=False)
    metoda = Column(String(10), nullable=False)
    konto = Column(String(50), nullable=True)
    wlasciciel_konta = Column(String(100), nullable=True)
    data = Column(Date, server_default=func.current_date())
    # checki
    __table_args__ = (
        CheckConstraint(typ.in_(['wplyw', 'wydatek']), name='check_typ_trans'),
        CheckConstraint(metoda.in_(['gotowka', 'przelew']), name='check_metoda_trans')
    )
    # relacje
    uzytkownik_fk = relationship("UzytkownikDB", back_populates='transakcje_fk')
    kategoria_fk = relationship("KategoriaDB", back_populates="transakcje_fk")

class PowtarzalnaDB(Base):
    __tablename__ = "t_t_powtarzalne"

    id_t_powtarzalnej = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # klucze
    id_uzytkownika = Column(Integer, ForeignKey("t_uzytkownik.id_uzytkownika", ondelete="CASCADE"), nullable=False)
    id_kategorii = Column(Integer, ForeignKey("t_kategorie.id_kategorii", ondelete="CASCADE"))
    # kolumny
    typ = Column(String(10), nullable=False)
    tytul = Column(String(100), nullable=False)
    opis = Column(Text, nullable=True)
    kwota = Column(Numeric(12, 2), nullable=False)
    metoda = Column(String(10), nullable=False)
    konto = Column(String(50), nullable=True)
    wlasciciel_konta = Column(String(100), nullable=True)
    co_ile = Column(String(10))
    nastepny_termin = Column(Date)
    czy_aktywna = Column(Boolean, default=True)
    # checki
    __table_args__ = (
        CheckConstraint(typ.in_(['wplyw', 'wydatek']), name='check_typ_powt'),
        CheckConstraint(metoda.in_(['gotowka', 'przelew']), name='check_metoda_powt')
    )
    # relacje
    uzytkownik_fk = relationship("UzytkownikDB", back_populates='powtarzalne_fk')
    kategoria_fk = relationship("KategoriaDB", back_populates="powtarzalne_fk")
