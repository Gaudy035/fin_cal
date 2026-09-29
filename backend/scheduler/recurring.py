from models import Recurring, Transaction
from database import SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler
import isodate
from datetime import datetime

def process_recurring():
    print(f'[{datetime.now()}] Sprawdzanie powtarzalnych')
    db = SessionLocal()
    try:
        now = datetime.now().date()
        payments = (
            db.query(Recurring)
            .filter(Recurring.next_date <= now, 
                Recurring.is_active == True)
            .all()
        )

        for rp in payments:
            try:
                interval = isodate.parse_duration(rp.interval)
            except Exception as e:
                print(f"Error for payment with ID:{rp.recurring_id} - {rp.title}:{rp.interval}")
                continue

            new_payment = Transaction(
                user_id = rp.user_id,
                category_id = rp.category_id,
                amount = rp.amount,
                title = rp.title,
                transaction_method = rp.transaction_method,
                description = rp.description,
                transaction_type = rp.transaction_type,
                transaction_date = rp.next_date,
                account = rp.account,
                account_owner = rp.account_owner
            )
            db.add(new_payment)

            rp.next_date += interval
            
            print(f"Processed {rp.title} for user {rp.user_id}")
        db.commit()

    except Exception as e:
        print(f"Process error: {e}")
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