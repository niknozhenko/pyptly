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


def response(request):
    """API response wrapper
    """
    try:
        msg = request.json()
    except ValueError as err:
        msg = {u'error': err}
    return msg
