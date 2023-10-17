from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel


class Forward(BaseModel):
    task_id: str
    is_new_task: bool
    plan: list
    payload: list

app = FastAPI()
random_url_suffix = uuid4().hex

@app.post(f"/{random_url_suffix}/forward")
def forward(forward: Forward):
    print("Forward request received: ", forward)

if __name__ == "__main__":
    input(r"""# Command to register the generated worker
-----------------------------------------
curl -X 'POST' \
  'http://127.0.0.1:8000/register_worker/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{""" + \
f"""  "worker_url": "http://127.0.0.1:8001/{random_url_suffix}" }}'
-----------------------------------------
Press enter to start the worker server...""")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
