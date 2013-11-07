"""Exceptions raised by ftw.tika.
"""


class ProcessError(Exception):
    """Raised if a spawned process terminated with exit code != 0.
    """


class TikaConversionError(Exception):
    """Raised if an error happened during conversion with Tika.
    """


class TikaJarNotConfigured(Exception):
    """Raised if no path to Tika JAR file was specified.
    """


class TikaJarNotFound(Exception):
    """Raised if a path to Tika JAR file was specified, but is invalid.
    """
