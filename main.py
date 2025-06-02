from fastapi import FastAPI, Depends,Query,HTTPException,Path
from sqlalchemy.orm import Session
from db import SessionLocal, init_db
from passlib.hash import bcrypt
from models import Client,User
from schemas import UserCreate,ClientCreate,ClientOut
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, get_current_user, oauth2_scheme


app = FastAPI()

def get_db():
    db :Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Clients API!"}

@app.get("/clients")
def get_clients(
    id :int = Query(None),
    name :str = Query(None),
    email :str = Query(None),
    db: Session = Depends(get_db)):

    query = db.query(Client)

    if id:
        query = query.filter(Client.id == id)
    if name:
        query = query.filter(Client.name == name)
    if email:
        query = query.filter(Client.email == email)

    clients = query.all()

    return [ 
        {"id": c.id, "name": c.name, "email": c.email, "phone_number": c.phone_number}
        for c in clients
    ]

@app.post("/clients",response_model=ClientOut)
def create_client(client_data: ClientCreate, db: Session=Depends(get_db),current_user: dict = Depends(get_current_user)):
    existing_client_email = db.query(Client).filter(Client.email == client_data.email ).first()
    existing_client_phone = db.query(Client).filter(Client.phone_number == client_data.phone_number).first()
    
    if existing_client_email:
        raise HTTPException(status_code=400,detail="This email is already used")
    
    if existing_client_phone:
        raise HTTPException(status_code=400,detail="This phone is already used")
    
    new_client = Client(
        name = client_data.name,
        email = client_data.email,
        phone_number = client_data.phone_number
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client

@app.put("/client/{id}",response_model=ClientOut)
def update_client(
    client_data : ClientCreate,
    id:int =Path(...,description="ID of the client to update"),
     current_user: dict = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    client = db.query(Client).filter(Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404,detail="Client not found")
    
    client.name = client_data.name
    client.email = client_data.email
    client.phone_number = client_data.phone_number

    db.commit()
    db.refresh(client)

    return client


@app.delete("/clients/{id}")
def delete_client(
    id: int = Path(...,description="ID of the client to delete"),
    current_user: dict = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
      
    client = db.query(Client).filter(Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404,detail="Client not found")
    
    db.delete(client)
    db.commit()

    return {"detail":f"Client with id {id} was deleted successfully"}

@app.post("/register")
def register(user_data: UserCreate,db:Session= Depends(get_db)):
    user_email = db.query(User).filter(User.email==user_data.email).first()

    if  user_email:
        raise HTTPException(status_code=400,detail="The user with same email already exists")
    
    hashed_password = bcrypt.hash(user_data.password)

    new_user = User(
        name = user_data.name,
        email = user_data.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{"detail": f"User {new_user.name} registered successfully"}


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not bcrypt.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['email']}, you have access!"}



@app.get("/clients_secure", response_model=list[ClientOut])
def get_clients_secure(
    id: int | None = Query(None),
    name: str | None = Query(None),
    email: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Client)
    if id is not None:
        query = query.filter(Client.id == id)
    if name:
        query = query.filter(Client.name == name)
    if email:
        query = query.filter(Client.email == email)

    clients = query.all()
    return clients
