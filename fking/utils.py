import hashlib
import os


def normalize_path(path) -> str:
    path = os.path.abspath(path)
    return path.replace("\\", '/')


def normalize_tags(tags: str) -> str:
    normalized: list[str] = []
    tags_split = tags.split(',')

    for tag in tags_split:
        _tag = tag.strip().lower()
        if _tag not in normalized:
            normalized.append(_tag)

    return ', '.join(normalized)


def sanitize_dirname(name: str) -> str:
    if name.isalnum():
        return name

    out = ''
    for ch in name:
        if ch.isalnum() or ch in ['-', '_', ' ', '\'']:
            out = out + ch
    return out


def normalize_alt_text(alt_text: str) -> str:
    tags_text = alt_text
    if " - " in alt_text and ("stock picture" in alt_text or "royalty-free" in alt_text):
        _alt_text = alt_text[:alt_text.rindex(" - ")].strip()
        _alt_text = normalize_tags(_alt_text)
        if len(_alt_text) > 0:
            tags_text = _alt_text

    return normalize_tags(tags_text)


def contains_partial(haystack: str, needle: str) -> bool:
    needle = needle.lower()
    haystack = haystack.lower()

    if needle in haystack:
        return True

    needles = needle.split()
    for split_n in needles:
        if split_n in haystack:
            return True

    return False


def write_binary(dst: str, binary):
    with open(dst, 'wb') as f:
        f.write(binary)
        f.close()


def write_text(dst: str, text: str):
    with open(dst, 'w') as f:
        f.write(text)
        f.close()


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()
