"""Read an openly accessible, unencrypted PalmDOC/MOBI in memory for research.

No source ebook is saved. Unsupported compression and encryption fail closed.
This is a small text-access utility, not an edition/provenance verifier.
"""
import argparse
import html
import re
import struct
import urllib.request


def decompress_palmdoc(data):
    result = bytearray()
    i = 0
    while i < len(data):
        value = data[i]
        i += 1
        if 1 <= value <= 8:
            result.extend(data[i:i + value])
            i += value
        elif value < 128:
            result.append(value)
        elif value < 192:
            if i == len(data):
                raise ValueError("Incomplete PalmDOC back-reference")
            pair = (value << 8) | data[i]
            i += 1
            distance = (pair & 0x3FFF) >> 3
            length = (pair & 7) + 3
            if distance == 0 or distance > len(result):
                raise ValueError("Invalid PalmDOC back-reference")
            for _ in range(length):
                result.append(result[-distance])
        else:
            result.extend((32, value ^ 128))
    return bytes(result)


def read_public_mobi(url):
    with urllib.request.urlopen(url, timeout=20) as response:
        data = response.read()
    count = struct.unpack_from(">H", data, 76)[0]
    starts = [struct.unpack_from(">I", data, 78 + 8 * i)[0] for i in range(count)]
    starts.append(len(data))
    header = data[starts[0]:starts[1]]
    compression, _, text_length, text_records = struct.unpack_from(">HHIH", header)
    encryption = struct.unpack_from(">H", header, 12)[0]
    if encryption:
        raise ValueError("Encrypted MOBI is not supported")
    if compression not in (1, 2):
        raise ValueError(f"Unsupported compression: {compression}")
    if header[16:20] != b"MOBI":
        raise ValueError("Not a recognized MOBI text header")
    codepage = struct.unpack_from(">I", header, 28)[0]
    encoding = {65001: "utf-8", 1252: "cp1252"}.get(codepage)
    if not encoding:
        raise ValueError(f"Unsupported codepage: {codepage}")
    mobi_length = struct.unpack_from(">I", header, 20)[0]
    mobi_version = struct.unpack_from(">I", header, 104)[0]
    flags = struct.unpack_from(">H", header, 242)[0] if mobi_length >= 228 and mobi_version >= 5 else 0
    # Trailer format checked against KindleUnpack's mobi_header.py getRawML:
    # https://github.com/kevinhendricks/KindleUnpack/blob/master/lib/mobi_header.py
    def trim_record(chunk):
        for _ in range((flags >> 1).bit_count()):
            size = 0
            for byte in chunk[-4:]:
                size = ((0 if byte & 128 else size) << 7) + (byte & 127)
            if size <= 0 or size >= len(chunk):
                raise ValueError("Invalid MOBI trailer length")
            chunk = chunk[:-size]
        if flags & 1:
            chunk = chunk[:-((chunk[-1] & 3) + 1)]
        return chunk
    chunks = [data[starts[i]:starts[i + 1]] for i in range(1, text_records + 1)]
    chunks = [trim_record(c) for c in chunks]
    raw = b"".join(decompress_palmdoc(c) if compression == 2 else c for c in chunks)
    if len(raw) != text_length:
        raise ValueError(f"Decoded text size mismatch: {len(raw)} != {text_length}")
    markup = raw[:text_length].decode(encoding)
    markup = re.sub(r"</(?:p|div|h[1-6]|li)>|<br\s*/?>", "\n", markup, flags=re.I)
    text = html.unescape(re.sub(r"<[^>]*>", "", markup))
    return text, {"compression": compression, "encryption": encryption,
                  "text_records": text_records, "text_length": text_length,
                  "encoding": encoding, "trailing_data_flags": flags}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--pattern", action="append", default=[])
    parser.add_argument("--context", type=int, default=800)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    text, metadata = read_public_mobi(args.url)
    print(metadata)
    if not args.pattern:
        print(text[:1500])
    for pattern in args.pattern:
        matches = list(re.finditer(re.escape(pattern), text, re.I))
        print(f"\nPATTERN {pattern!r}: {len(matches)} matches")
        for match in matches[:args.limit]:
            print(f"\nCHAR {match.start()}\n{text[max(0, match.start()-args.context):match.end()+args.context]}")
