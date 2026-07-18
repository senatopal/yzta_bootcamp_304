from pydantic import BaseModel

class HealthCheck(BaseModel):
    status: str
    database: str
    project_name: str
