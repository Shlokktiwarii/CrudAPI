from fastapi import FastAPI,HTTPException, Body, Response

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
@app.get("/tasks",summary="Get all tasks")
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
@app.post('/tasks',status_code=201, summary="Create new tasks")
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

@app.put("/tasks/{id}", summary="Update the tasks")
def update_task(id: int, body: dict):
    for task in tasks:
        if task["id"] == id:

            if not body:
                raise HTTPException(status_code=400, detail="Request body is empty")

            if "title" in body:
                task["title"] = body["title"]

            if "done" in body:
                task["done"] = body["done"]

            return task

    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", status_code=204 , summary="Delete tasks")
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail="Task not found")