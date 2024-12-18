from uuid import UUID

from pydantic import BaseModel


class InstitutionSchema(BaseModel):
    id: UUID
    name: str


class StudentSchema(BaseModel):
    id: UUID
    name: str
    institution: InstitutionSchema


class StudentIDRequestBodySchema(BaseModel):
    ids: str
    institution_id: UUID | None = None
