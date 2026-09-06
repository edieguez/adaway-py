# CLAUDE.md

A small Python 3 CLI that blocks ads by rewriting the system hosts file. One runtime
dependency (colorama).

## Layout

`__main__.py` parses flags and dispatches to `lib/util.py`, which orchestrates everything
else:

| Module | Responsibility |
| --- | --- |
| `lib/config.py` | `config.json` (`host_files`, `blacklist`, `whitelist`, `custom_hosts`) and path resolution |
| `lib/network.py` | Downloads a source list, keeps the hostname out of each `IP hostname` line |
| `lib/database.py` | SQLite store, single `blacklist(hostname UNIQUE)` table |
| `lib/filesystem.py` | Writes the hosts file |
| `lib/termcolor.py` | Coloured `[i]` / `[w]` / `[e]` output |

## Things that are not obvious from the code

**`adaway.py` is a build artifact, not source.** It is a zipapp (shebang + zip) bundling
`__main__.py`, `lib/`, and a vendored colorama, and it is committed to the repo — it is what
the README tells users to download. It goes stale the moment `lib/` changes, so rebuild it
with `./build.sh` and commit it alongside the source change.

**There are two apply paths, and the difference is deliberate.**
`fully_apply_host_blocking()` (`lib/util.py:56`, the no-flag default) re-downloads every
source and rebuilds the table from scratch. `apply_host_blocking()` (`lib/util.py:25`)
re-exports from the existing database and only downloads if the database is missing. The
whitelist/blacklist mutators call the cheap path on purpose — editing a list should not
trigger four downloads.

The full refresh clears the table before repopulating, so hosts dropped upstream stop being
blocked. It skips the clear when every download failed, so a network outage leaves the
existing database intact rather than emptying the hosts file.

**State lives beside the entry point** — `config.json` and `adaway.db`. `lib/config.py`
resolves this by walking up from `__file__` and checking whether the package root is a file,
which is how a zipapp presents itself (`.../adaway.py/lib/config.py`). Both a source checkout
and the zipapp land in the same place. Don't "simplify" that check away.

**Editing the defaults in `Config.write_default()` only affects new installs.** Existing
users keep whatever `config.json` they already have.

**Whitelist entries cover subdomains** (`_is_exempt` in `lib/database.py`), so `adf.ly` also
exempts `www.adf.ly` but not `notadf.ly`.

## Testing

Never test by writing the real hosts file. `-o` redirects the output:

```sh
python3 . -o /tmp/hosts          # source checkout
./adaway.py -o /tmp/hosts        # zipapp
```

Unit tests need pytest, which isn't in the runtime requirements:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```

Tests import `from lib import ...`, so run them from the repo root. `tests/` touches no
network and no real files — `network` is patched, everything else writes to `tmp_path`.

## Out of scope

No `pyproject.toml` / PyPI packaging. Distribution is the committed zipapp; changing that is
a project decision, not a cleanup.
