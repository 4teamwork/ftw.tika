"""Utility functions for ftw.tika.
"""

from ftw.tika.exceptions import ProcessError
import re
import subprocess


def run_process(cmd):
        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # wait for the process to terminate
        stdout, stderr = process.communicate()
        errcode = process.returncode

        if errcode != 0:
            raise ProcessError(stderr)

        return (stdout, stderr)


def clean_extracted_plaintext(text, filename=''):
    """Clean up raw plain text returned by either Tika Server or a local tika
    app by removing common noise that we don't want in the extracted text,
    like word bookmark names or filenames of thumbnails.
    """
    text = strip_word_bookmarks(text, filename)
    return text


def strip_word_bookmarks(text, filename=''):
    """Newer versions of tika also include Word bookmarks in the returned
    plain text. They are inserted in the form
    '[bookmark: Foo][bookmark: _GoBack]Lorem Ipsum'

    For our purpose of building the searchable text, we want to strip those.
    """
    if not filename.lower().endswith('.docx'):
        return text

    pattern = re.compile(r'\[bookmark:.*?\]')
    text = re.sub(pattern, '', text)
    return text
