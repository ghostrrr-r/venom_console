#!/usr/bin/env python3
import base64

# ---- Put your encoded string here ----
encoded_string = "3031313030303031303130303031313130313031313031303031313030313130303130313130303130313031303131303031303130303130303130313031303030313130303031313031313031313030303130303031313030313030313030313031303130313131303130313130303030313031303131303030313130313030303131303030313130313130313130313031313030313030303131313031313030313031303131303031303030313131303131313031303030313031313031303031313030303131303131303131303130313130313030303031313031303031303130313031303030313030303131313031303030313130303130313030303030313130303030313031303130313131303130303130313030303131303031303031313030303031303031313030313030303131303030313030313130303130303130313030303130313130313130313031313030313030303130303130313030313130303130303030313130303130303130313031313030303131303031303031303130303130303131303031313130303131313130313030313131313031"  # replace with yours

def try_binary(s):
    if all(c in '01' for c in s) and len(s) % 8 == 0:
        try:
            b = bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))
            return b.decode('utf-8')
        except Exception:
            return None
    return None

def try_hex(s):
    if all(c in '0123456789abcdefABCDEF' for c in s) and len(s) % 2 == 0:
        try:
            return bytes.fromhex(s).decode('utf-8')
        except Exception:
            return None
    return None

def try_base64(s):
    try:
        decoded = base64.b64decode(s)
        return decoded.decode('utf-8')
    except Exception:
        return None

def smart_decode(s):
    """Try decoding multiple times until result looks human-readable."""
    prev = s.strip()
    for _ in range(5):  # try up to 5 layers
        for func in (try_binary, try_hex, try_base64):
            decoded = func(prev)
            if decoded and decoded != prev:
                prev = decoded.strip()
                break
        else:
            break
    return prev

decoded = smart_decode(encoded_string)

print("Decoded output:\n")
print(decoded)
