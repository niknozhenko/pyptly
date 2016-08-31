import requests
from pyptly.utils import prefix_sanitized, response
from .conf import assert_is_instance, assert_equals

def test_prefix():
    test_map = ( ('.', ':.'),
                 ('a.', 'a.'),
                 ('a.a', 'a.a'),
                 ('.a', '.a'),
                 (':.', ':.'),
                 ('.1', '.1'),
                 ('..', '..'),
                 ('_', '__'),
                 ('a_', 'a__'),
                 ('_a', '__a'),
                 ('__', '__'),
                 ('__.', '__.'),
                 ('_a_', '__a__'),
                 ('__a', '__a'),
                 ('a__', 'a__'),
                 ('_._', '__.__'),
                 ('/', '_'),
                 ('a/', 'a_'),
                 ('/a', '_a'),
                 ('/_', '___'),
                 ('_/', '___'),
                 ('/-', '_-'),
                 ('-/', '-_'),
                 ('./.', '._.'),
                 ('//', '__'),
                 ('//_', '____') )

    for test_val, expect_val in test_map:
        assert_equals(prefix_sanitized(test_val), expect_val)


def test_response():
    request = requests.get('https://api.github.com')
    assert_is_instance(response(request), dict)

    request = requests.get('https://google.com')
    msg = response(request, meta_msg='error')
    assert_is_instance(msg, dict)
    assert_equals(msg['meta'], 'error')
