from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from contextlib import asynccontextmanager

from database import get_session, init_db
from auth import authenticate_user, create_access_token, get_current_user, get_current_admin, get_password_hash
from models import User
from schemas import TicketCreate, TicketRead, Token
import services


# Db initialize
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# Create FastAPI app
app = FastAPI(title="TicketFlow API", version="1.0", lifespan=lifespan)


# Authentication endpoint
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# Register new user
@app.post("/register")
def register(username: str, password: str, session: Session = Depends(get_session)):
    from auth import get_user_by_username
    if get_user_by_username(username, session):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created"}


# Create ticket
@app.post("/tickets", response_model=TicketRead)
def create_ticket_endpoint(
    ticket_in: TicketCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return services.create_ticket(ticket_in.title, ticket_in.description, current_user.id, session)


# User views their own tickets
@app.get("/tickets/my", response_model=list[TicketRead])
def get_my_tickets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return services.get_tickets(session, owner_id=current_user.id)


# Admin view for tickets
@app.get("/tickets", response_model=list[TicketRead])
def get_all_tickets(
    admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    return services.get_tickets(session)


# Admin updates ticket status
@app.patch("/tickets/{ticket_id}")
def update_status(
    ticket_id: int,
    status: str,
    admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    ticket = services.update_ticket_status(ticket_id, status, session)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    return {"message": f"Ticket {ticket_id} status updated to {status}"}
