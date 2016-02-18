import re

import requests


def strip_html_tag(text):
    """
    text(str) -> str

    Remove HTML Tags from given text.
    Reference: http://stackoverflow.com/a/4869782/4754787
    WARNING: This is UNSAFE. There may be issues with the method.
    """
    return re.sub('<[^<]+?>', '', text)


def strip_white_space(text):
    """
    text(str) -> str

    Remove all duplicate whitespaces, \\n and \\t
    """
    return ' '.join(text.split())


class Endpoint(object):
    """
    Define an endpoint of duty list resource.
    """

    def __init__(self, url, name):
        self.url = url
        self.name = name

        self._response = None
        self._text = ''

    def request(self):
        res = requests.get(self.url)
        self._response = res

        # M$ Word generated HTML contains some weird HTML tag in names.
        # No idea why it does that. Anyway, these extra tags have to be
        # stripped.
        self._text = strip_white_space(strip_html_tag(res.text))

    def __contains__(self, key):
        """
        Perform a RegExp search by the given key.
        Invoked by using 'in' operator.

        :return -- Bool, if there is a match of RegExp of given string.
        """
        match = re.search(key, self._text, re.I)
        return match is not None
