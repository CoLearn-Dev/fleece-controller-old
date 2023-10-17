# Golden Fleece - Controller

## Test OpenAI API

- In the first terminal, run the controller server:
```sh
python main.py
```

> Note: do NOT use ```uvicorn main:app --reload``` to start the server, as it won't start the scheduler process.

- In the second terminal, copy the worker registration command (it is not necessary to press enter here):
```sh
python test_worker_integration.py
```

- In the third terminal, paste the command and execute:
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/register_worker/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{  "worker_url": "http://127.0.0.1:8001/<REPLACE_HERE>" }'
```

- Return to the second terminal, and press enter to start the dummy worker server if you haven't done it before.

- In the fourth terminal, run:
```sh
python test_chat_completions.py
```

You should be able to observe meaningful logs in all terminals.

## Controller API docs

- In the terminal:
```sh
python main.py
```
- Then visit http://127.0.0.1:8000/docs
