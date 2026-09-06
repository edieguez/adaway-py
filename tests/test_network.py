from unittest.mock import patch

from lib import network

SAMPLE = '\n'.join([
    '# This is a comment',
    '',
    '0.0.0.0 ads.example',
    '127.0.0.1 tracker.example',
    '127.0.0.1\ttabbed.example',
    '0.0.0.0 trailing.example # inline comment',
    'not-an-ip host.example',
    '999.999.999.999 stillmatches.example',
    '0.0.0.0',
    '   0.0.0.0 indented.example',
])


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return self._payload


def _download(payload):
    with patch.object(network.request, 'urlopen', return_value=_Response(payload)):
        return network.download_file('https://example.invalid/hosts.txt')


def test_parses_hosts_lines():
    domains = _download(SAMPLE.encode('utf-8'))

    assert 'ads.example' in domains
    assert 'tracker.example' in domains
    assert 'tabbed.example' in domains
    assert 'trailing.example' in domains


def test_skips_comments_blank_lines_and_malformed_rows():
    domains = _download(SAMPLE.encode('utf-8'))

    assert 'host.example' not in domains
    assert 'indented.example' not in domains
    assert not any(domain.startswith('#') for domain in domains)
    assert '' not in domains


def test_handles_windows_line_endings():
    payload = '0.0.0.0 ads.example\r\n0.0.0.0 more.example\r\n'.encode('utf-8')

    assert _download(payload) == ['ads.example', 'more.example']


def test_sends_an_identifying_user_agent():
    with patch.object(network.request, 'urlopen', return_value=_Response(b'')) as urlopen:
        network.download_file('https://example.invalid/hosts.txt')

    sent = urlopen.call_args.args[0]
    assert sent.get_header('User-agent') == network.USER_AGENT


def test_network_failure_returns_an_empty_list():
    with patch.object(network.request, 'urlopen', side_effect=OSError('unreachable')):
        assert network.download_file('https://example.invalid/hosts.txt') == []


def test_timeout_returns_an_empty_list():
    with patch.object(network.request, 'urlopen', side_effect=TimeoutError('timed out')):
        assert network.download_file('https://example.invalid/hosts.txt') == []
