from fastapi import FastAPI,HTTPException, Body

app = FastAPI()

tasks = [
    {"id":1,"title":"Learn FastAPI","done":False},
    {"id":2,"title":"Build FastAPI","done":False},
    {"id":3,"title":"Deploy Project","done":True}
]
@app.get("/")
def root():
    return { "name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] 
            }
@app.get("/health")
def health():
    return{
        "status":"ok"
    }
@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
           return task
    raise HTTPException(
        status_code=404 , 
        detail={"error":f"Task{id} not found"}
    )
@app.post('/tasks',status_code=201)
def create_task(task:dict =Body(...)):
    if "title" not in task or task["title"].strip() == "":
         raise HTTPException(
            status_code=400,
            detail={"error": "Title is required"}
        )

    
    new_id = len(tasks) + 1

   
    new_task = {
        "id": new_id,
        "title": task["title"],
        "done": False
    }

  
    tasks.append(new_task)

    return new_task
        
