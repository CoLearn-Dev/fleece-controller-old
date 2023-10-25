import openai
import datetime
import json

# from openai_secret import API_BASE, API_KEY
from llama.tokenizer import Tokenizer  # LATER: move to a separate file
llama_enc = Tokenizer("./llama/tokenizer.model")

API_BASE = "http://127.0.0.1:8000/v1"
API_KEY = "DUMMY"  # To bypass the API key check from the openai package
MODEL = "llama-2-7b-chat"

TEST_CONTENT = "Hvad er Keto? Og er det ikke usundt kun at spise kød?"

def main():
    # test streaming completion
    input("[Test streaming mode] Press enter to continue...")
    completion = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": TEST_CONTENT}],
        model=MODEL,
        stream=True,
        api_base=API_BASE,
        api_key=API_KEY,
    )
    previous = []
    for chunk in completion:
        # print the chunk with the current timestamp
        timestamp_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{timestamp_str} {json.dumps(chunk.choices, indent=None)}")
        token = chunk.choices[0]["delta"]["content"]
        if token:
            previous.append(token)
        # if len(previous) % 128 == 0:
        #     print(llama_enc.sp_model.decode(previous))
        #     input("Continue >>>")
    # test non-streaming completion
    input("[Test non-streaming mode] Press enter to continue...")
    completion = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": TEST_CONTENT}],
        model=MODEL,
        api_base=API_BASE,
        api_key=API_KEY,
    )
    print(completion)


if __name__ == "__main__":
    main()
