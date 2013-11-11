"""Utilities used in tests.
"""


class RaisingConverter(object):
    """Used to replace the ftw.tika.converter.TikaConverter with a thing that
    conforms to the same interface, but just raises a defined exception once
    the convert() method is called.
    """

    def __init__(self, exception):
        self.exception = exception

    def convert(self, doc, *args, **kwargs):
        raise self.exception
