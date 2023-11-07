# Golden Fleece - Controller

## Test OpenAI API

- In the first terminal, run the controller server:
```sh
python main.py
```

> Note: do NOT use ```uvicorn main:app --reload``` to start the server, as it won't start the scheduler process.

- In the second terminal, run the dummy worker and follow the prompt:
```sh
python test_worker_integration.py
```

- In the third terminal, run:
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
