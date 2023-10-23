import requests
import time
import random
import multiprocessing
from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel

from llama.tokenizer import Tokenizer  # LATER: move to a separate file
enc = Tokenizer("./llama/tokenizer.model")


class Forward(BaseModel):
    task_id: str
    is_new_task: bool
    plan: list
    payload: list


app = FastAPI()
server_url = "http://127.0.0.1:8000"
# random_url_suffix = uuid4().hex
random_url_suffix = "ad1240607e2b4cea81675af543ac8381"
access_token = multiprocessing.Array("c", 1024)

def mock_plan_executor(q, access_token):
    # mock output for a single worker consuming the complete plan
    while True:
        forward_req: Forward = q.get()
        # simulate delayed responses
        my_plan = forward_req.plan[0]
        assert random_url_suffix in my_plan[0], f"url_suffix does not match: '{random_url_suffix}' not in '{my_plan[0]}'"
        output_s = f"From dummy worker: generating output for task_id={forward_req.task_id}."
        for token in enc.encode(output_s, bos=False, eos=True):
            time.sleep(random.randint(5, 10) / 100.)
            for layer in my_plan[1]:
                time.sleep(random.randint(5, 10) / 100.)
                response = requests.post(
                    f"{server_url}/update_task/",
                    headers={"worker-token": f"{access_token.value.decode()}"},
                    json={
                        "t_id": forward_req.task_id,
                        "stat": {
                            "updated_layer": layer,
                        },
                        "output_token": [token] if layer == my_plan[1][-1] else None,
                    }
                )
                print(f"-- update_task-response received: ", response.json())

Q = multiprocessing.Queue()
P = multiprocessing.Process(target=mock_plan_executor, args=(Q, access_token))

@app.post("/{url_suffix}/forward")
def forward(url_suffix: str, forward_req: Forward):
    print(f"<{url_suffix}> forward-request received: ", forward_req)
    Q.put(forward_req)

if __name__ == "__main__":
    P.start()
    c = input(r"""# Command to register the generated worker
-----------------------------------------
curl -X 'POST' """ + f'\'{server_url}/register_worker/' + r"""' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{""" + \
f"""  "worker_url": "http://127.0.0.1:8001/{random_url_suffix}" }}'
-----------------------------------------
Would you like to automatically register the worker? [y]/n: """)
    if c == "" or c == "y":
        response = requests.post(
            f"{server_url}/register_worker/",
            json={"worker_url": f"http://127.0.0.1:8001/{random_url_suffix}"}
        )
        print("Worker registered: ", response.json())
        access_token.value = response.json()["access_token"].encode()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
