import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from models import Client, BASE


DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

st.title("Clients Dashboard 📊")

db = SessionLocal()

clients = db.query(Client).all()

df_clients = pd.DataFrame([
    {"id": c.id, "name": c.name, "email": c.email, "phone_number": c.phone_number}
    for c in clients
])


search = st.text_input("🔎 Search by name or email or phone number")

if search:
    df_clients = df_clients[
        df_clients["name"].str.contains(search, case=False) |   
        df_clients["email"].str.contains(search, case=False) |
        df_clients["phone_number"].str.contains(search,case=False)
    ]


st.dataframe(df_clients)
st.write(f"Total clients: {len(df_clients)}")

