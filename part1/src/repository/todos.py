from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.todo import ContactSchema, ContactUpdateSchema
from sqlalchemy.sql.expression import or_
from datetime import datetime, timedelta


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    #stmt = select(Contact).offset(offset).limit(limit)
# async def get_contacts(limit: int, offset: int, db: AsyncSession):
#     stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
# async def get_contact(contact_id: int, db: AsyncSession):
#     stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def search_contact(contact_query: str, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(user=user).filter(
# async def search_contact(contact_query: str, db: AsyncSession):
#     stmt = select(Contact).filter(
        or_(Contact.first_name.ilike(f"%{contact_query}%"), Contact.last_name.ilike(f"%{contact_query}%"),
            Contact.email.ilike(f"%{contact_query}")))
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)  
# async def create_contact(body: ContactSchema, db: AsyncSession):
#     contact = Contact(**body.model_dump(exclude_unset=True))      
    
    # (title=body.title, description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


#async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        # contact.title = body.title
        contact.first_name = body.first_name
        # contact.description = body.description
        contact.last_name = body.last_name
        # contact.completed = body.completed
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info              
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
# async def delete_contact(contact_id: int, db: AsyncSession):
#     stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact



async def contacts_upcoming_birthdays(db: AsyncSession, user: User):
    current_date = datetime.now().date()
    week_later = current_date + timedelta(days=7)
    stmt = select(Contact).filter_by(user=user).filter(Contact.birthday.between(current_date, week_later)).order_by(Contact.birthday)
    # stmt = select(Contact).filter(Contact.birthday.between(current_date, week_later)).order_by(Contact.birthday)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()












