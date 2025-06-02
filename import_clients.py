import pandas as pd
from sqlalchemy.orm import Session
from models import Client
from db import SessionLocal, init_db
from pathlib import Path
import os 

MAIN_PATH = Path()
file_path = MAIN_PATH / "data"/"clients.xlsx"
init_db()

db:Session = SessionLocal()

df = pd.read_excel(file_path,skiprows=1)
df.columns = df.columns.str.lower()

for _,row in df.iterrows():
    client = Client(
        id = int(row["id"]),
        name = row['name'],
        email = row['email'],
        phone_number = row['phone_number']
    )
    if not db.query(Client).filter(Client.id == client.id).first():
        db.add(client)
    else:
        print("SAME ID DETECTED")   

db.commit()
db.close()
print("Migration done")