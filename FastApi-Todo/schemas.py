from pydantic import BaseModel

class TodoBase(BaseModel):
    title:str | None = None
    description:str | None = None
    completed:bool = False


class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id:int
    class config:
        orm_mode = True