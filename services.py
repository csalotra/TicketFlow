from sqlmodel import Session, select
from models import Ticket, User
from typing import List, Optional



# Ticket Services
def create_ticket(title: str, description: str, owner_id: int, session: Session) -> Ticket:
    """
    Create a new ticket owned by the given user.
    """
    ticket = Ticket(title=title, description=description, owner_id=owner_id)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

def get_tickets(session: Session, owner_id: Optional[int] = None) -> List[Ticket]:
    """
    Retrieve all tickets.
    - If owner_id is given, only return that user's tickets.
    - If not, return all (for admins).
    """
    statement = select(Ticket)
    if owner_id:
        statement = statement.where(Ticket.owner_id == owner_id)
    return session.exec(statement).all()


def get_ticket_by_id(ticket_id: int, session: Session) -> Optional[Ticket]:
    """
    Retrieve a specific ticket by ID.
    """
    return session.get(Ticket, ticket_id)


def update_ticket_status(ticket_id: int, new_status: str, session: Session) -> Optional[Ticket]:
    """
    Update the status of a ticket (open → closed, etc.).
    Only admins should use this function.
    """
    ticket = get_ticket_by_id(ticket_id, session)
    if not ticket:
        return None
    ticket.status = new_status
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket
