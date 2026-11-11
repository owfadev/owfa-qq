import os


def _text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def verify(ctx):
    """Read-only check that the connector carries the 0.3 hygiene layer."""
    issues = []
    base = os.path.join(ctx.root, "connectors", "qq-cli")

    gateway = _text(os.path.join(base, "qqcli", "gateway.py"))
    if gateway and "def _note(" not in gateway:
        issues.append(("warning", "gateway.py has no listener logging — update/reinstall the connector"))

    store = _text(os.path.join(base, "qqcli", "store.py"))
    if store and "_purge_sent" not in store:
        issues.append(("warning", "store.py does not roll sent.jsonl — update/reinstall the connector"))

    watcher = _text(os.path.join(base, "scripts", "qq-agent-watch.py"))
    if watcher and "consecutive_failures" not in watcher:
        issues.append(("warning", "watcher has no failure breaker — update/reinstall the connector"))
    if watcher and "^  status:" not in watcher:
        issues.append(("warning", "watcher cron-status regex not unified — update/reinstall the connector"))

    return issues
