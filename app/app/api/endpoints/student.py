from uuid import UUID

from fastapi import APIRouter
from fastapi_sqlalchemy_toolkit import comma_list_query, get_comma_list_values
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.api.deps import Session
from app.models import ServiceBStudent
from app.schemas import StudentIDRequestBodySchema, StudentSchema

router = APIRouter()


@router.get("")
async def get_students(
    session: Session,
    ids: comma_list_query,
    institution_id: UUID | None = None,
    limit: int = 20,
) -> list[StudentSchema]:
    stmt = (
        select(ServiceBStudent)
        .where(ServiceBStudent.id.in_(get_comma_list_values(ids, UUID)))
        .options(joinedload(ServiceBStudent.institution))
        .limit(limit)
    )
    if institution_id:
        stmt = stmt.filter_by(institution_id=institution_id)
    return (await session.execute(stmt)).scalars().all()  # type: ignore


@router.post("/ids")
async def get_student_ids(
    session: Session, in_obj: StudentIDRequestBodySchema
) -> list[UUID]:
    ids_list = get_comma_list_values(in_obj.ids, UUID)
    if not in_obj.institution_id or not in_obj.ids:
        return ids_list
    stmt = select(ServiceBStudent.id).order_by(ServiceBStudent.created_at)
    if in_obj.ids:
        stmt = stmt.where(ServiceBStudent.id.in_(ids_list))
    if in_obj.institution_id:
        stmt = stmt.where(ServiceBStudent.institution_id == in_obj.institution_id)
    return (await session.execute(stmt)).scalars().all()
