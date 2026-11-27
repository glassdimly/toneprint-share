#!/usr/bin/env python3
"""Read and write TC Electronic TonePrint export files (.tpr) that you made yourself.

This tool ships no key material. It finds the key string in your own
installed copy of TonePrint Editor: you supply one .tpr that the editor
exported for you, and the tool uses it to check each candidate string.

Commands:
  tpr.py findkey --exe TonePrint.exe --sample MINE.tpr
        print the key string; then export TPR_KEY_STRING=... for the other commands
  tpr.py decode FILE.tpr > FILE.json      .tpr -> JSON text
  tpr.py encode FILE.json > FILE.tpr      JSON text -> .tpr (checksum included)
  tpr.py dump FILE.tpr                    list the toneprintData words, numbered
  tpr.py set FILE.tpr OUT.tpr NAME WORD=VALUE [WORD=VALUE ...]
        copy FILE.tpr with a new name, a new toneprintId and changed words

See FORMAT.md for the file layout and what the words mean.
"""
import os
import re
import secrets
import struct
import sys

# CRC-16/MODBUS (reflected poly 0xA001, init 0xFFFF, no final xor), nibble table.
CRC_TABLE = [0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
             0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400]
WORDS_START = 20  # byte offset of word 0 inside toneprintData


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for c in data:
        crc = (crc >> 4) ^ CRC_TABLE[(crc ^ c) & 0xF]
        crc = (crc >> 4) ^ CRC_TABLE[(crc ^ (c >> 4)) & 0xF]
    return crc


def keystream(s: bytes) -> bytes:
    n = len(s)
    return bytes(s[j] ^ s[n - 1 - j] for j in range(n))


def crypt(body: bytes, ks: bytes) -> bytes:
    return bytes(c ^ ks[i % len(ks)] for i, c in enumerate(body))


def decode(raw: bytes, ks: bytes) -> bytes:
    if crc16(raw[2:]) != int.from_bytes(raw[:2], "big"):
        print("warning: file checksum mismatch", file=sys.stderr)
    return crypt(raw[2:], ks)


def encode(text: bytes, ks: bytes) -> bytes:
    body = crypt(text, ks)
    return crc16(body).to_bytes(2, "big") + body


def find_key(exe: str, sample: str) -> bytes:
    """Try every printable run in the editor binary until one decodes the sample."""
    body = open(sample, "rb").read()[2:]
    blob = open(exe, "rb").read()
    # The key is stored as a standalone printable string, so try whole runs only.
    for m in re.finditer(rb"[\x20-\x7e]{32,1024}", blob):
        cand = m.group(0)
        ks = keystream(cand)
        if crypt(body[:16], ks) == b'{ "toneprintId" ' and \
                b'"toneprintData"' in crypt(body, ks):
            return cand
    sys.exit("no key found: is the sample a .tpr exported by this editor version?")


def load_key() -> bytes:
    k = os.environ.get("TPR_KEY_STRING")
    if not k:
        sys.exit("set TPR_KEY_STRING first (run: tpr.py findkey --exe ... --sample ...)")
    return keystream(k.encode())


def data_hex(text: bytes) -> str:
    return re.search(rb'"toneprintData" : "([0-9a-f]+)"', text).group(1).decode()


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd = a[0]
    if cmd == "findkey":
        opts = dict(zip(a[1::2], a[2::2]))
        print(find_key(opts["--exe"], opts["--sample"]).decode())
        return
    ks = load_key()
    if cmd == "encode":
        sys.stdout.buffer.write(encode(open(a[1], "rb").read(), ks))
    elif cmd == "decode":
        sys.stdout.buffer.write(decode(open(a[1], "rb").read(), ks))
    elif cmd == "dump":
        b = bytes.fromhex(data_hex(decode(open(a[1], "rb").read(), ks)))
        print("header:", b[:4].hex(), "name:", b[4:20].split(b"\0")[0].decode("latin1"))
        for n, i in enumerate(range(WORDS_START, len(b) - 3, 4)):
            print(n, struct.unpack(">i", b[i:i + 4])[0])
    elif cmd == "set":
        src, out, name, *assigns = a[1:]
        text = decode(open(src, "rb").read(), ks).decode("latin1")
        h = data_hex(text.encode("latin1"))
        b = bytearray(bytes.fromhex(h))
        for kv in assigns:
            w, v = (int(x) for x in kv.split("="))
            b[WORDS_START + 4 * w:WORDS_START + 4 * w + 4] = struct.pack(">i", v)
        if len(name.encode()) > 15:
            sys.exit("name must be 15 bytes or fewer")
        b[4:20] = name.encode().ljust(16, b"\0")
        text = text.replace(h, b.hex())
        text = re.sub(r'"toneprintName" : "[^"]*"', f'"toneprintName" : "{name}"', text)
        text = re.sub(r'"toneprintId" : "[0-9a-f]{32}"',
                      f'"toneprintId" : "{secrets.token_hex(16)}"', text)
        open(out, "wb").write(encode(text.encode("latin1"), ks))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
