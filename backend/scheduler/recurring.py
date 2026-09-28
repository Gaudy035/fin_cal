import models
from database import SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler
import isodate
from datetime import datetime

def process_recurring():
    print(f'[{datetime.now()}] Sprawdzanie powtarzalnych')
    db = SessionLocal()
    try:
        now = datetime.now().date()
        payments = db.query(models.PowtarzalnaDB).filter(models.PowtarzalnaDB.nastepny_termin<=now, models.PowtarzalnaDB.czy_aktywna==True).all()

        for rp in payments:
            try:
                interval = isodate.parse_duration(rp.co_ile)
            except Exception as e:
                print(f"Blad Formatu dla platnosci ID:{rp.id_t_powtarzalnej} - {rp.tytul}:{rp.co_ile}")
                continue

            new_payment = models.TransakcjaDB(
                id_uzytkownika = rp.id_uzytkownika,
                id_kategorii = rp.id_kategorii,
                kwota = rp.kwota,
                tytul = rp.tytul,
                metoda = rp.metoda,
                opis = rp.opis,
                typ = rp.typ,
                data = rp.nastepny_termin,
                konto = rp.konto,
                wlasciciel_konta = rp.wlasciciel_konta
            )
            db.add(new_payment)

            rp.nastepny_termin+=interval
            
            print(f"Przetworzono {rp.tytul} dla {rp.id_uzytkownika}")
        db.commit()

    except Exception as e:
        print(f"Blad podczas przetwarzania: {e}")
        db.rollback()
    finally:
        db.close()

scheduler = BackgroundScheduler()

def start_scheduler():
    print("SCHEDULER START")
    scheduler.start()
    scheduler.add_job(process_recurring, 'interval', hours=12)
    process_recurring()

def stop_scheduler():
    print("SCHEDULER STOP")
    scheduler.shutdown()