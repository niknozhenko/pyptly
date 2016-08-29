import re

def prefix_sanitized(prefix):
    """Change prefix in accordance with Aptly Publish APIs convention
    https://www.aptly.info/doc/api/publish/
    """
    # replace '.' with ':.'
    prefix = re.sub('^\.$', ':.', prefix)
    # replace single underscores with double underscores
    prefix = re.sub('(?<!_)_(?!_)', '__', prefix)
    # replace slashes with single underscores
    prefix = re.sub('/', '_', prefix)
    return prefix
