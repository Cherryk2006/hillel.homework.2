import os
import smtplib

import db
from celery import Celery
from sqlalchemy import select

from app import db_connector
from database import init_db

app = Celery('tasks', broker=f'pyamqp://guest:guest@{os.environ.get("RABBITMQ_HOST", "localhost")}//')

@app.task
def add(x, y):
    print(x + y)


def select(Item):
    pass


def send_email(models=None, items=None):
    import smtplib
    from email.message import EmailMessage

    init_db()

    contracts = db_connector.select('contracts')

    items_query = select(models.Item)
    items = list(db.session.execute(items).scalars())


    msg = EmailMessage()
    msg.set_content(f"My mega long message")

    msg['Subject'] = f'New contract about item {items.name}'
    msg['From'] = "service_email@gmail.com"
    msg['To'] = "user1@example.com"

    s = smtplib.SMTP('localhost')
    s.send_message(msg)

    msg['To'] = "user2@example.com"
    s.send_message(msg)

    s.quit()
