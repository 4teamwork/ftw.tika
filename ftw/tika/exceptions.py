"""Exceptions raised by ftw.tika.
"""


class ProcessError(Exception):
    """Raised if a spawned process terminated with exit code != 0.
    """


class TikaConversionError(Exception):
    """Raised if an error happened during conversion with Tika.

    May contain additional information about the error on the Tika side:
    - status_code: The HTTP status code returned by the Tika JAXRS server
    - stack_trace: The Java stack trace from the tika-app.jar, or, if
      available, from the Tika JAXRS Server
    """
    def __init__(self, message, status_code=None, stack_trace=None):
        self.message = message
        self.status_code = status_code
        self.stack_trace = stack_trace

    def __str__(self):
        return self.message


class TikaJarNotConfigured(Exception):
    """Raised if no path to Tika JAR file was specified.
    """


class TikaJarNotFound(Exception):
    """Raised if a path to Tika JAR file was specified, but is invalid.
    """
