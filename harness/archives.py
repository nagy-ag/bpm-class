"""Bounded ZIP extraction for untrusted lesson data; never executes content."""
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

MAX_FILES = 10000
MAX_BYTES = 256 * 1024 * 1024
MAX_MEMBER = 64 * 1024 * 1024
PRIVATE_NAMES = {'.env', '.env.local', '.git', '.bpa', '.codex', '.ssh', '.aws',
                 'credentials.json', 'cookies.json', 'cookies.sqlite', 'login data',
                 'web data', 'key4.db', 'logins.json'}


def private_part(name):
    name = name.casefold()
    return name in PRIVATE_NAMES or name.startswith('.env.') or name.endswith(('.pem', '.key', '.pfx'))


def linked(path):
    return path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction())


def safe_parts(name):
    # Backslashes are separators on Windows, regardless of the ZIP producer.
    name = name.replace('\\', '/')
    if name.startswith('/') or ':' in name or any(ord(c) < 32 for c in name):
        raise ValueError('ZIP contains an absolute, drive or control-character path.')
    parts = name.rstrip('/').split('/')
    if not parts or any(p in ('', '.', '..') or p.endswith((' ', '.')) for p in parts):
        raise ValueError('ZIP contains an unsafe or ambiguous path.')
    for part in parts:
        if re.fullmatch(r'(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', part, re.I):
            raise ValueError('ZIP contains a reserved Windows filename.')
        if any(c in part for c in '<>"|?*') or private_part(part):
            raise ValueError('ZIP contains a private or unsupported filename.')
    return PurePosixPath(*parts).parts


def extract_zip(archive, destination):
    """Prevalidate every member, then extract to a NEW directory. No extractall."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Extraction requires a new isolated directory.')
    with zipfile.ZipFile(archive) as z:
        members = z.infolist()
        if len(members) > MAX_FILES or sum(i.file_size for i in members) > MAX_BYTES:
            raise ValueError('ZIP expansion limit exceeded.')
        seen = set()
        checked = []
        for item in members:
            parts = safe_parts(item.filename)
            key = '/'.join(parts).casefold()
            mode = item.external_attr >> 16
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError('ZIP links and special files are not allowed.')
            if key in seen:
                raise ValueError('ZIP has duplicate or case-colliding paths.')
            seen.add(key)
            if item.flag_bits & 1 or item.file_size > MAX_MEMBER:
                raise ValueError('Encrypted or oversized ZIP member.')
            if item.file_size > 1024 * 1024 and item.file_size / max(item.compress_size, 1) > 1000:
                raise ValueError('ZIP compression ratio exceeds the safe limit.')
            checked.append((item, parts))
        destination.mkdir(parents=True)
        for item, parts in checked:
            path = destination.joinpath(*parts)
            if item.is_dir():
                path.mkdir(parents=True, exist_ok=True)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            with z.open(item) as source, path.open('xb') as target:
                remaining = item.file_size
                while remaining:
                    chunk = source.read(min(1024 * 1024, remaining))
                    if not chunk:
                        raise ValueError('Truncated ZIP member.')
                    target.write(chunk)
                    remaining -= len(chunk)
                if source.read(1):
                    raise ValueError('ZIP member exceeds its declared size.')
    return destination
