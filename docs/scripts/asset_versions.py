"""Keep cached documentation assets in sync with the generated HTML."""

from hashlib import sha256
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def on_config(config, **_kwargs):
    for setting in ("extra_css", "extra_javascript"):
        versioned = []
        for asset in config[setting]:
            url = urlsplit(asset)
            source = Path(config.docs_dir) / url.path
            if not url.netloc and not url.scheme and source.is_file():
                query = [(key, value) for key, value in parse_qsl(url.query) if key != "content"]
                query.append(("content", sha256(source.read_bytes()).hexdigest()[:16]))
                asset = urlunsplit(url._replace(query=urlencode(query)))
            versioned.append(asset)
        config[setting] = versioned
    return config
