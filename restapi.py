from fastapi import FastAPI, Request, Body
from celery.result import AsyncResult
from tasks import generate_pdf_task
from typing import Dict, Any
import os

app = FastAPI()

@app.post("/generate_receipt")
async def generate_receipt(data: Dict[str, Any] = Body(..., example={
    "shop_name": "Aray Mini-Market",
    "items": [
        {"name": "Bread", "price": 150, "qty": 2},
        {"name": "Beer", "price": 300, "qty": 1}
    ]
})):
    # Задача в селери
    task = generate_pdf_task.delay(data)
    return {"task_id": task.id, "status": "processing"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    print(os.path.exists(f'C:/Users/user/Python Files/fastapi_course/receipts/receipt_{task_id}.pdf'))
    return {"task_id": task_id, "status": "completed" if os.path.exists(f'C:/Users/user/Python Files/fastapi_course/receipts/receipt_{task_id}.pdf') else "not found"} 