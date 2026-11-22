"""Exact research feature functions for the final R2 candidate; no model fitting."""
import re
import ipaddress
from urllib.parse import urlsplit
import numpy as np

n02_normalization_pattern = re.compile(
    r"(?P<prefix>https?://|//)?(?P<authority>[^/?#]+)(?P<suffix>[/?#].*)?",
    flags=re.IGNORECASE,
)
n02_exp13_unreserved = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)


def n02_url_view(texts, part="full"):
    result = []
    for text in texts:
        text = str(text)
        try:
            parsed = urlsplit(text if "://" in text else "//" + text)
            value = (
                text
                if part == "full"
                else (
                    (parsed.hostname or "")
                    if part == "host"
                    else parsed.path + "?" + parsed.query + "#" + parsed.fragment
                )
            )
        except ValueError:
            value = text if part == "full" else "__parse_error__"
        result.append(value or "__empty__")
    return result

def n02_url_structure(texts):
    rows = []

    for text in texts:
        text = str(text).strip()

        try:
            parsed = urlsplit(
                text if "://" in text or text.startswith("//")
                else "//" + text
            )
            host = parsed.hostname or ""
            path = parsed.path
            query = parsed.query
            fragment = parsed.fragment
            has_userinfo = parsed.username is not None
            parse_failed = False
        except ValueError:
            host, path, query, fragment = "", "", "", ""
            has_userinfo = False
            parse_failed = True

        try:
            ipaddress.ip_address(host)
            host_is_ip = True
        except ValueError:
            host_is_ip = False

        length = max(len(text), 1)
        host_labels = [part for part in host.split(".") if part]
        path_parts = [part for part in path.split("/") if part]

        counts = [
            len(text), len(host), len(path), len(query), len(fragment),
            len(host_labels), len(path_parts),
            max((len(part) for part in host_labels), default=0),
            max((len(part) for part in path_parts), default=0),
        ]

        proportions = [
            sum(char.isdigit() for char in text) / length,
            sum(char.isalpha() for char in text) / length,
            sum(ord(char) > 127 for char in text) / length,
        ]

        punctuation = [
            text.count(char)
            for char in (".", "-", "_", "/", "?", "&", "=", "%", "@")
        ]

        flags = [
            bool(query), bool(fragment), has_userinfo,
            host_is_ip, parse_failed,
        ]

        # Compress count ranges; scaling is fitted separately per fold.
        rows.append(
            np.log1p(counts).tolist()
            + proportions
            + np.log1p(punctuation).tolist()
            + [float(flag) for flag in flags]
        )

    return np.asarray(rows, dtype=np.float32)

def n02_hostcase_identity(text):
    parsed = urlsplit(
        text if "://" in text or text.startswith("//")
        else "//" + text
    )
    return (
        parsed.scheme.lower(),
        parsed.hostname,
        parsed.port,
        parsed.username,
        parsed.password,
        parsed.path,
        parsed.query,
        parsed.fragment,
    )

def n02_normalize_host_one(text):
    text = str(text)
    match = n02_normalization_pattern.fullmatch(text)

    if match is None:
        return text, False

    prefix = match.group("prefix") or ""
    authority = match.group("authority")
    suffix = match.group("suffix") or ""

    # Preserve user information exactly; isolate the hostname and port.
    userinfo, separator, hostport = authority.rpartition("@")
    userinfo_prefix = userinfo + separator if separator else ""

    if not re.fullmatch(
        r"[A-Za-z0-9.-]+(?::[0-9]+)?", hostport
    ):
        return text, False

    host, port_separator, port = hostport.partition(":")
    if not host:
        return text, False

    try:
        parsed = urlsplit(
            text if prefix else "//" + text
        )
        if parsed.hostname != host.lower():
            return text, False
        parsed.port  # Reject invalid port numbers.
    except ValueError:
        return text, False

    normalized_authority = (
        userinfo_prefix
        + host.lower()
        + (port_separator + port if port_separator else "")
    )
    normalized = prefix + normalized_authority + suffix

    # Only ASCII hostname case may change.
    assert normalized_authority.lower() == authority.lower()
    assert (
        n02_hostcase_identity(normalized)
        == n02_hostcase_identity(text)
    )

    return normalized, True

def n02_path_equivalence_form(path):
    def replace_triplet(match):
        character = chr(int(match.group(0)[1:], 16))
        return (
            character
            if character in n02_exp13_unreserved
            else match.group(0)
        )

    return re.sub(r"%[0-9A-Fa-f]{2}", replace_triplet, path)

def n02_normalize_host_path_one(text):
    """Normalize hostname case and ASCII unreserved path encodings only."""
    host_normalized, supported = n02_normalize_host_one(text)
    if not supported:
        return text, False

    match = n02_normalization_pattern.fullmatch(host_normalized)
    if match is None:
        return text, False

    prefix = match.group("prefix") or ""
    authority = match.group("authority")
    suffix = match.group("suffix") or ""

    # Preserve query and fragment exactly as written.
    boundary = re.search(r"[?#]", suffix)
    path_end = boundary.start() if boundary else len(suffix)
    path = suffix[:path_end]
    remainder = suffix[path_end:]

    # Leave the entire input unchanged when path escapes are malformed.
    if re.search(r"%(?![0-9A-Fa-f]{2})", path):
        return text, False

    normalized_path = n02_path_equivalence_form(path)
    normalized = prefix + authority + normalized_path + remainder
    return normalized, True

def n02_normalize_host_path_batch(texts):
    """Return normalized classifier inputs without dropping unsupported URLs."""
    return [n02_normalize_host_path_one(text)[0] for text in texts]
