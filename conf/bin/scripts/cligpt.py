#!/usr/bin/env python3
from keyring import set_password, get_password
from getpass import getuser
from requests import get, session
from requests.structures import CaseInsensitiveDict
from sys import argv

auth_url = "https://api.openai.com/v1/completions"

data = {
    "model": "text-davinci-003",
    "prompt": None,
    "max_tokens": 7,
    "temperature": 0.7,
    "n": 1,
    "stream": False,
    "logprobs": None,
    "stop": "\n",
}


def write_api_key(api_key):
    set_password("cligpt", getuser(), api_key)


def get_prompt(prompt):
    data["prompt"] = prompt
    return data


def post_query(sess, headers, prompt):
    data["prompt"] = prompt
    r = sess.post(auth_url, headers=headers, json=data)
    resp = r.json()
    if r.status_code != 200:
        if len(resp) == 1 and "error" in resp:
            print("Error: %s" % resp["error"]["message"])
        else:
            print("Request error: %s" % r.status_code)
        exit(1)
    return resp


def main():
    if not len(argv) == 2:
        print("Usage: cligpt.py <prompt>")
        exit(1)

    if not get_password("cligpt", getuser()):
        api_key = input("Enter your OpenAI API key: ")
        write_api_key(api_key)

    api_key = get_password("cligpt", getuser())
    prompt = argv[1]

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer %s" % api_key

    while True:
        with session() as sess:
            print(post_query(sess, headers, prompt)["choices"][0]["text"])
            prompt = input(">>> ")
            if prompt == "exit":
                exit(0)


if __name__ == "__main__":
    main()
