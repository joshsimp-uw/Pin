from fastapi import APIRouter
from models.ticket import Ticket

router = APIRouter()

fake_tickets = [
    Ticket(id=1, title="Printer not working", status="open"),
    Ticket(id=2, title="Cannot login", status="closed"),
]

@router.get("/", response_model=list[Ticket])
def get_tickets():
    return fake_tickets
