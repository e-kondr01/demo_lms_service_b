from fastapi_sqlalchemy_toolkit import ModelManager

from app.models import Student
from app.schemas import StudentSchema

student_manager = ModelManager[Student, StudentSchema, StudentSchema](Student)
