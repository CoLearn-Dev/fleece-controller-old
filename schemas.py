from typing import Optional, Literal, List
from pydantic import BaseModel, RootModel


class WorkerRegister(BaseModel):
    worker_url: str

class WorkerToken(BaseModel):
    access_token: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatMessageList(RootModel):
    root: List[ChatMessage]
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

class ChatCompletionRequest(BaseModel):
    model: str
    messages: ChatMessageList
    # temperature: float | None = 1
    # top_p: float | None = 1
    n: int | None = 1
    stream: bool | None = False
    # stop: list | None = None
    # max_tokens: int | None = None
    # presence_penalty: float | None = 0
    # frequency_penalty: float | None = 0
    # logit_bias: dict | None = None
    # user: str | None = None

class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[Literal["stop", "length"]] = None

class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: Optional[int] = 0
    total_tokens: int = 0

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo

class DeltaMessage(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None

class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage = DeltaMessage()
    finish_reason: Optional[Literal["stop", "length"]] = None

class ChatCompletionStreamResponse(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionResponseStreamChoice]

class TaskUpdate(BaseModel):
    t_id: str
    # TODO: shall we add next token index here? (probably also changes forward-calling procedure)
    status: str = None
    output_token: Optional[List[int]] = None
    stat: dict = {}
