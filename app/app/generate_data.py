import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_factory
from app.models import (
    ServiceBInstitution,
    ServiceBStudent,
)

institution_names = (
    "ИТМО",
    "ТюмГУ",
    "Политех",
    "МГУ",
    "МФТИ",
    "СПбГУ",
    "МИФИ",
    "МГУТ им. Баумана",
    "ВШЭ",
    "МГИМО",
)


async def generate_institutions(session: AsyncSession):
    for name in institution_names:
        institution = ServiceBInstitution(name=name)
        session.add(institution)
    await session.commit()


async def generate_students(session: AsyncSession):
    for index, name in enumerate(institution_names):
        institution = (
            await session.execute(select(ServiceBInstitution).filter_by(name=name))
        ).scalar_one()
        for i in range(1, (index + 1) * 100 + 1):
            student = ServiceBStudent(
                name=f"Студент {institution.name} {i+1}", institution_id=institution.id
            )
            session.add(student)

    await session.commit()


async def main():
    async with async_session_factory() as session:
        await generate_institutions(session)
        await generate_students(session)


asyncio.run(main())
