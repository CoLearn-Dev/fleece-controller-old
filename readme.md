# Golden Fleece - Controller

## Test OpenAI API

- In the first terminal:
```sh
python main.py
```

> Note: do NOT use ```uvicorn main:app --reload``` to start the server, as it won't start the scheduler process.

- In the second terminal:
```sh
python test_worker_integration.py
```

- In the third terminal, copy paste the worker registration command from the second terminal:
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/register_worker/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{  "worker_url": "http://127.0.0.1:8001/<REPLACE_HERE>" }'
```

- In the fourth terminal:
```sh
python test_chat_completions.py
```

You should be able to observe meaningful logs in the all terminals.

## API docs

- In the terminal:
```sh
python main.py
```
- Then visit http://127.0.0.1:8000/docs
