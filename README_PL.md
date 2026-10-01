# Monitor Finansowy

Aplikacja webowa do monitorowania finansów. Umożliwia śledzenie nadchodzących transakcji, historii przeszłych i dodawanie nowych, w tym cyklicznych powtarzających się automatycznie. Ma mozliwosc wyswietlania wykresów bilansu wpływów i wydatków na obecny miesiąc, a także wydatków podzielonych na kategorie.

## Technologie

- **FRONTEND:** React, TypeScript, Vite, TailwindCSS, Bun
- **BACKEND:** FastAPI, SQLAlchemy, Alembic, APScheduler
- **BAZA DANYCH:** PostgreSQL
- **DEPLOYMENT:** Docker, Nginx

## Wymagania

- Docker
  lub lokalnie:
- Python 3.14, Bun, PostgreSQL 16

## Zmienne srodowiskowe:

### `.env` - Baza danych (Docker)

| Zmienna             | Opis                   |
| ------------------- | ---------------------- |
| `POSTGRES_DB`       | Nazwa bazy danych      |
| `POSTGRES_USER`     | Użytkownik bazy danych |
| `POSTGRES_PASSWORD` | Haslo użytkownika      |

### `backend/.env`

| Zmienna             | Opis                                          |
| ------------------- | --------------------------------------------- |
| `DB_USER`           | Użytkownik bazy danych                        |
| `DB_PASS`           | Hasło użytkownika bazy danych                 |
| `DB_HOST`           | Serwer bazy danych dla developmentu lokalnego |
| `DB_PORT`           | Port serwera bazy danych                      |
| `DB_NAME`           | Nazwa bazy danych                             |
| `SECRET_KEY`        | Klucz uzywany dla tokenow JWT                 |
| `TOKEN_EXPIRE_MINS` | Czas zycia tokena JWT w minutach              |

### `frontend/.env` (serwer lokalny) | `frontend/.env.production` (Docker)

| Zmienna        | Opis               |
| -------------- | ------------------ |
| `VITE_API_URL` | Adres API backendu |

Tu nalezy utworzyc dwa pliki zgodnie z `.env.example`.

**.env** dla serwera lokalnego (np. `http://127.0.0.1:8000`) i **.env.production** dla Dockera (np. `http://localhost/api`)

## Uruchamianie przez Docker

Utwórz i uzupelnij pliki `.env` zgodnie z example i opisem powyżej

Migracje bazy danych (Alembic) uruchamiają się automatycznie przy starcie backendu.

Przy pierwszym uruchomieniu:

```bash
docker-compose up --build
```

Przy nastepnych uruchomieniach:

```bash
docker-compose up
```

## Uruchamianie lokalnie

Utwórz i uzupelnij pliki `.env` zgodnie z example i opisem powyżej

### FRONTEND

Przy pierwszym uruchomieniu:

```bash
bun install
bun run dev
```

Przy nastepnych uruchomieniach:

```bash
bun run dev
```

### BACKEND

Przy pierwszym uruchomieniu:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Przy następnych uruchomieniach:

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

### BAZA DANYCH

Uruchom serwer PostgreSQL, utwórz bazę danych i uruchom migracje:

```bash
alembic upgrade head
```

### TESTY

Testy backendu (pytest) uruchamiasz z katalogu `backend`:

```bash
pytest
```

Kolekcja zapytań API znajduje się w `backend/postman`.

## Struktura projektu

```bash
fin_cal/
├── backend          # FastAPI
│   ├── alembic      # Migracje bazy danych
│   ├── models       # Modele SQLAlchemy
│   ├── routers      # Endpointy API
│   ├── schemas      # Schematy Pydantic
│   ├── services     # Logika biznesowa
│   ├── security     # Autoryzacja i hasła
│   ├── scheduler    # Zadania cykliczne (APScheduler)
│   ├── tests        # Testy pytest
│   └── postman      # Kolekcja Postmana
├── frontend         # React
└── docker-compose.yaml
```