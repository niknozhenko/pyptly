"""
pyptly.utils
-----------

Miscellaneous module tools
"""
import re

def prefix_sanitized(prefix):
    """Change prefix in accordance with Aptly Publish APIs convention
    https://www.aptly.info/doc/api/publish/
    """
    # replace '.' with ':.'
    prefix = re.sub(r'^\.$', ':.', prefix)
    # replace single underscores with double underscores
    prefix = re.sub(r'(?<!_)_(?!_)', '__', prefix)
    # replace slashes with single underscores
    prefix = re.sub(r'/', '_', prefix)
    return prefix


def response(request, meta_msg=None):
    """API respose wrapper
    """
    meta_msg = meta_msg if meta_msg else u'Operation aborted'
    try:
        msg = request.json()
    except ValueError:
        msg = {u'meta': meta_msg,
               u'error': u'response code - {0}'.format(request.status_code)}
    return msg
