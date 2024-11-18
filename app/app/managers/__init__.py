from fastapi_sqlalchemy_toolkit import ModelManager

from app.models import ServiceBStudent
from app.schemas import StudentSchema

student_manager = ModelManager[ServiceBStudent, StudentSchema, StudentSchema](
    ServiceBStudent
)
