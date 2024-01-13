from uuid import UUID

from fastapi import APIRouter
from fastapi_sqlalchemy_toolkit import comma_list_query, get_comma_list_values
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.api.deps import Session
from app.models import Student
from app.schemas import StudentSchema

router = APIRouter()


@router.get("")
async def get_students(
    session: Session,
    ids: comma_list_query,
    institution_id: UUID | None = None,
    limit: int = 20,
) -> list[StudentSchema]:
    stmt = (
        select(Student)
        .where(Student.id.in_(get_comma_list_values(ids, UUID)))
        .options(joinedload(Student.institution))
        .limit(limit)
    )
    if institution_id:
        stmt = stmt.filter_by(institution_id=institution_id)
    return (await session.execute(stmt)).scalars().all()  # type: ignore


@router.get("/ids")
async def get_students_for_paginated_assessments(
    session: Session,
    ids: comma_list_query,
    institution_id: UUID | None = None,
) -> list[UUID]:
    ids_list = get_comma_list_values(ids, UUID)
    if not institution_id or not ids:
        return ids_list
    stmt = select(Student.id).where(
        Student.institution_id == institution_id, Student.id.in_(ids_list)
    )
    return (await session.execute(stmt)).scalars().all()
