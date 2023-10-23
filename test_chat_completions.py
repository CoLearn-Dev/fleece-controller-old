import openai
import datetime
import json

# from openai_secret import API_BASE, API_KEY

API_BASE = "http://127.0.0.1:8000/v1"
API_KEY = "DUMMY"  # To bypass the API key check from the openai package
MODEL = "llama-2-7b-chat"

def main():
    # test streaming completion
    input("[Test streaming mode] Press enter to continue...")
    completion = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": "Tell me a joke."}],
        model=MODEL,
        stream=True,
        api_base=API_BASE,
        api_key=API_KEY,
    )
    for chunk in completion:
        # print the chunk with the current timestamp
        timestamp_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{timestamp_str} {json.dumps(chunk.choices, indent=None)}")
    # test non-streaming completion
    input("[Test non-streaming mode] Press enter to continue...")
    completion = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": "Tell me a joke."}],
        model=MODEL,
        api_base=API_BASE,
        api_key=API_KEY,
    )
    print(completion)


if __name__ == "__main__":
    main()
