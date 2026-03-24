from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler
import isodate
from routers import users, stats, categories, transactions, recurring
from datetime import datetime

# region scheduler

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

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("SCHEDULER START")
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(process_recurring, 'interval', hours=12)
    process_recurring()
    yield
    print("SCHEDULER STOP")
    scheduler.shutdown()

# endregion scheduler

app = FastAPI(lifespan=lifespan)

# region routery

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(stats.router)
app.include_router(transactions.router)
app.include_router(recurring.router)

# endregion routery

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)