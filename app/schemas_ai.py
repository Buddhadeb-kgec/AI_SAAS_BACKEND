from pydantic import BaseModel


class AIResultOut(BaseModel):
    id: int
    content: str
    ai_output: str

    class Config:
        from_attributes = True
