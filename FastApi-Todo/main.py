from fastapi import FastAPI, Depends, HTTPException
from schemas import TodoCreate, TodoResponse
from sqlalchemy.orm import Session
from database import Sessionlocal, Base, engine
from models import TodoModel
app = FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos",response_model=TodoResponse)
def create_todo(todo : TodoCreate,db:Session = Depends(get_db)):
    new_todo = TodoModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

    

@app.get("/todos",response_model=list[TodoResponse])
def Read_todo(db:Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@app.get("/todos/{todo_id}",response_model=TodoResponse)
def Read_single_todo(todo_id:int, db: Session = Depends(get_db)):
    readsingledata = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not readsingledata :
        raise HTTPException(status_code = 404,detail= "Todo not found")
    return readsingledata

@app.put("/todos/{todo_id}",response_model=TodoResponse)
def update_todo(todo_id:int,Updated:TodoCreate,db:Session = Depends(get_db)):
    update = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not update:
        raise HTTPException(status_code = 404,detail= "Todo not found")
    for key,value in Updated.dict().items():
        setattr(update,key,value)
        db.commit()
        db.refresh(update)
    return update
    
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db:Session = Depends(get_db)):
    delete = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if(not delete):
        raise HTTPException(status_code = 404,detail= "Todo not found")
    db.delete(delete)
    db.commit()
    return {"detail":"Todo deleted successfully"}