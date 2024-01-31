import string

TIME_QUALIFIERS = {
    "ns": 1,
    "us": 1000,
    "ms": 1000 * 1000,
    "s": 1000 * 1000 * 1000,
    "m": 1000 * 1000 * 1000 * 60
}

BYTES_QUALIFIERS = {
    "b": 1,
    "kb": 1000,
    "mb": 1000 * 1000,
    "gb": 1000 * 1000 * 1000,
    "tb": 1000 * 1000 * 1000 * 1000
}


NUMERIC = string.digits + "."


def parse(src: str, qualifiers: dict[str, int] | None = None) -> float:
    if qualifiers is None:
        qualifiers = TIME_QUALIFIERS

    for i, char in enumerate(src):
        if char not in NUMERIC:
            return float(src[:i]) * qualifiers[src[i:]]

    return float(src)


def serialize(value: float, qualifiers: dict[str, int] | None = None) -> str:
    if qualifiers is None:
        qualifiers = TIME_QUALIFIERS

    prev = ""

    for qualifier, multiplier in qualifiers.items():
        if value < multiplier:
            return _float_with_qualifier(value / qualifiers[prev], prev)

        prev = qualifier

    qualifier = max(zip(qualifiers.values(), qualifiers.keys()))[1]

    return _float_with_qualifier(value / qualifiers[qualifier], qualifier)


def _float_with_qualifier(f: float, qualifier: str) -> str:
    if f.is_integer():
        f = int(f)

    return str(f) + qualifier
