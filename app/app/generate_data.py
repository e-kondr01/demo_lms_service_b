import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_factory
from app.models import ServiceBInstitution, ServiceBStudent


async def generate_institutions(session: AsyncSession):
    institution_names = ("ИТМО", "ТюмГУ", "Политех", "ФТМИ")
    for name in institution_names:
        institution = ServiceBInstitution(name=name)
        session.add(institution)
    await session.commit()


async def generate_students(session: AsyncSession):
    institution = (
        await session.execute(select(ServiceBInstitution).filter_by(name="ИТМО"))
    ).scalar_one()
    for i in range(200):
        student = ServiceBStudent(
            name=f"Студент ИТМО {i+1}", institution_id=institution.id
        )
        session.add(student)

    institution = (
        await session.execute(select(ServiceBInstitution).filter_by(name="ТюмГУ"))
    ).scalar_one()
    for i in range(100):
        student = ServiceBStudent(
            name=f"Студент ТюмГУ {i+1}", institution_id=institution.id
        )
        session.add(student)

    institution = (
        await session.execute(select(ServiceBInstitution).filter_by(name="Политех"))
    ).scalar_one()
    for i in range(180):
        student = ServiceBStudent(
            name=f"Студент Политеха {i+1}", institution_id=institution.id
        )
        session.add(student)

    institution = (
        await session.execute(select(ServiceBInstitution).filter_by(name="ФТМИ"))
    ).scalar_one()
    for i in range(230):
        student = ServiceBStudent(
            name=f"Студент ФТМИ {i+1}", institution_id=institution.id
        )
        session.add(student)

    await session.commit()


async def main():
    async with async_session_factory() as session:
        await generate_institutions(session)
        await generate_students(session)


asyncio.run(main())
