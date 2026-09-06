import json
import os

import pytest

from lib.config import Config


@pytest.fixture
def config(tmp_path, monkeypatch):
    monkeypatch.delenv('WINDIR', raising=False)

    config = Config('/tmp/hosts')
    config.config = str(tmp_path / 'config.json')
    config.write_default()

    return config


def test_default_config_has_the_four_sections(config):
    with open(config.config) as raw:
        body = json.load(raw)

    assert sorted(body) == ['blacklist', 'custom_hosts', 'host_files', 'whitelist']


def test_default_sources_use_https(config):
    assert all(source.startswith('https://') for source in config.read_key('host_files'))


def test_modify_key_round_trip(config):
    config.modify_key('whitelist', ['adf.ly'])

    assert config.read_key('whitelist') == ['adf.ly']


def test_modify_key_ignores_unknown_keys(config):
    config.modify_key('nonexistent', ['value'])

    with pytest.raises(KeyError):
        config.read_key('nonexistent')


def test_file_exists(tmp_path, monkeypatch):
    monkeypatch.delenv('WINDIR', raising=False)

    config = Config('/tmp/hosts')
    config.config = str(tmp_path / 'config.json')

    assert not config.file_exists()

    config.write_default()
    assert config.file_exists()


def test_explicit_hosts_file_wins(monkeypatch):
    monkeypatch.setenv('WINDIR', r'C:\Windows')

    assert Config('/tmp/hosts').hosts_file == '/tmp/hosts'


def test_windows_hosts_file_is_used_when_windir_is_set(monkeypatch):
    monkeypatch.setenv('WINDIR', 'C:/Windows')

    assert Config(None).hosts_file == os.path.join('C:/Windows', 'System32', 'Drivers', 'etc', 'hosts')


def test_hosts_file_defaults_to_etc_hosts(monkeypatch):
    monkeypatch.delenv('WINDIR', raising=False)

    assert Config(None).hosts_file == '/etc/hosts'


def test_state_files_live_beside_the_entry_point(monkeypatch):
    """A source checkout must not scatter state into the parent directory."""
    monkeypatch.delenv('WINDIR', raising=False)

    config = Config(None)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    assert os.path.dirname(config.config) == repo_root
    assert os.path.dirname(config.database) == repo_root
