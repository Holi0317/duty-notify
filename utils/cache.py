import os

CACHE_DIR = 'cache'


def make_cache(name, content):
    """
    Create cache with given content.

    :param str name -- Name, or key of the cache.
    :param str content -- Content of the cache
    :return bool -- If True, the content is changed with previously cached
    content. I.E. should process the updated content.
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    path = os.path.join(CACHE_DIR, name)

    if not os.path.exists(path):
        return _write_cache(name, content)

    with open(path, 'r') as file:
        read = file.read()

    if content == read:
        return False
    else:
        return _write_cache(name, content)


def _write_cache(name, content):
    """
    Write content into cache.
    :return bool -- True.
    """
    with open(os.path.join(CACHE_DIR, name), 'w') as file:
        file.write(content)
    return True
