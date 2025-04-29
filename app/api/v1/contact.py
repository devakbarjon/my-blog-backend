from fastapi import APIRouter, Depends, HTTPException, Form

from pydantic import EmailStr

from app.models.schemas.contacts import ContactForm
from app.models.contact import ContactRequest
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(
    prefix="/api/v1/contact",
    tags=["Contact"]
)

async def parse_contact_form(
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...)
) -> ContactForm:
    return ContactForm(name=name, email=email, message=message)


@router.post("/")
async def contact_submit(form: ContactForm = Depends(parse_contact_form), db: AsyncSession = Depends(get_db)):
    """
    Submit a contact form.
    """
    try:
        contact_request = ContactRequest(name=form.name, email=form.email, message=form.message)
        db.add(contact_request)
        await db.commit()
        await db.refresh(contact_request)
        return {"message": "Message sent successfully."}
    except Exception as e:
        print(f"Error submitting contact form: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    