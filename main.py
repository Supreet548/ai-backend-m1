from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

notes = [] #temporary memory database

class Note(BaseModel):
    title : str
    content : str


@app.get("/")
def home():
    return {"message":"Notes API Running"}

@app.post("/notes")
def create_note(note:Note):
    note_data = note.model_dump()
    note_data["id"]= len(notes)+1
    notes.append(note_data)
    return {"message":"Note created", "data": note_data}

@app.get("/notes")
def get_notes():
    return notes


@app.put("/notes/{note_id}")
def update_notes(note_id:int,note:Note):
    for item in notes:
        if item["id"]==note_id:
            item["title"]=note.title
            item["content"]=note.content
            return {"message":"Note updated","data":item}
    return {"error":"Note not found"}
    
@app.delete("/notes/{note_id}")
def delete_note(note_id:int):
    for item in notes:
        if item["id"]==note_id:
            notes.remove(item)
            return{"message":"Note deleted"}
    return{"error":"Note not found"}        
