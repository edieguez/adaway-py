from lib.database import Database


def _database(tmp_path, hosts=()):
    database = Database(str(tmp_path / 'adaway.db'))
    database.create_default_database()
    database.populate_database(list(hosts))

    return database


def test_database_exists(tmp_path):
    database = Database(str(tmp_path / 'adaway.db'))
    assert not database.database_exists()

    database.create_default_database()
    assert database.database_exists()


def test_blocked_hosts_are_sorted(tmp_path):
    database = _database(tmp_path, ['b.example', 'a.example'])

    assert database.get_blocked_hosts([]) == ['a.example', 'b.example']


def test_duplicated_hosts_are_ignored(tmp_path):
    database = _database(tmp_path, ['ads.example', 'ads.example'])
    database.populate_database(['ads.example'])

    assert database.get_blocked_hosts([]) == ['ads.example']


def test_whitelist_removes_an_exact_match(tmp_path):
    database = _database(tmp_path, ['adf.ly', 'other.example'])

    assert database.get_blocked_hosts(['adf.ly']) == ['other.example']


def test_whitelist_removes_subdomains(tmp_path):
    database = _database(tmp_path, ['adf.ly', 'www.adf.ly', 'a.b.adf.ly'])

    assert database.get_blocked_hosts(['adf.ly']) == []


def test_whitelist_does_not_match_a_suffix_of_another_domain(tmp_path):
    database = _database(tmp_path, ['notadf.ly', 'myadf.ly'])

    assert database.get_blocked_hosts(['adf.ly']) == ['myadf.ly', 'notadf.ly']


def test_localhost_is_always_exempt(tmp_path):
    database = _database(tmp_path, ['localhost', 'ads.example'])

    assert database.get_blocked_hosts([]) == ['ads.example']


def test_whitelist_argument_is_not_mutated(tmp_path):
    database = _database(tmp_path, ['ads.example'])
    whitelist = ['adf.ly']

    database.get_blocked_hosts(whitelist)

    assert whitelist == ['adf.ly']


def test_clear_empties_the_table(tmp_path):
    database = _database(tmp_path, ['ads.example', 'other.example'])

    database.clear()

    assert database.get_blocked_hosts([]) == []


def test_clear_then_populate_drops_stale_hosts(tmp_path):
    database = _database(tmp_path, ['gone.example', 'kept.example'])

    database.clear()
    database.populate_database(['kept.example'])

    assert database.get_blocked_hosts([]) == ['kept.example']
