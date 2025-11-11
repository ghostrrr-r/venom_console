#!/usr/bin/env python3
import os
import json
import urllib.request

# Get shared API key (same as main console)
import base64

# Encoded API key (hex -> binary -> base64 -> key)
encoded_string = "3031313030303031303130303031313130313031313031303031313030313130303130313130303130313031303131303031303130303130303130313031303030313130303031313031313031313030303130303031313030313030313030313031303130313131303130313130303030313031303131303030313130313030303131303030313130313130313130313031313030313030303131313031313030313031303131303031303030313131303131313031303030313031313031303031313030303131303131303131303130313130313030303031313031303031303130313031303030313030303131313031303030313130303130313030303030313130303030313031303130313131303130303130313030303131303031303031313030303031303031313030313030303131303030313030313130303130303130313030303130313130313130313031313030313030303130303130313030313130303130303030313130303130303130313031313030303131303031303031303130303130303131303031313130303131313130313030313131313031"

# Decode the API key
binary_string = bytes.fromhex(encoded_string).decode('utf-8')
b64_bytes = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
b64_string = b64_bytes.decode('utf-8')
api_key = base64.b64decode(b64_string).decode('utf-8')

# Same model you used before (omit :novita if that tag doesn't exist)
model = "MiniMaxAI/MiniMax-M2"

# OpenAI-style endpoint provided by Hugging Face router
url = "https://router.huggingface.co/v1/chat/completions"

# Build the request body
body = {
    "model": model,
    "messages": [
        {"role": "user", "content": "What is the capital of France?"}
    ],
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# Make the POST request
req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        # Print only the message text if present
        if "choices" in data and data["choices"]:
            print(data["choices"][0]["message"]["content"])
        else:
            print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP error {e.code}: {e.reason}")
    print(e.read().decode()[:800])
except Exception as e:
    print("Request failed:", e)
