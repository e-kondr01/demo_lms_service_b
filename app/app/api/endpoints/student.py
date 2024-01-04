from uuid import UUID

from fastapi import APIRouter
from fastapi_sqlalchemy_toolkit import comma_list_query, get_comma_list_values
from sqlalchemy.orm import joinedload

from app.api.deps import Session
from app.managers import student_manager
from app.models import Student
from app.schemas import StudentSchema

router = APIRouter()


@router.get("")
async def get_students(session: Session, ids: comma_list_query) -> list[StudentSchema]:
    return await student_manager.filter(
        session,
        where=(Student.id.in_(get_comma_list_values(ids, UUID))),
        options=joinedload(Student.institution),
    )
