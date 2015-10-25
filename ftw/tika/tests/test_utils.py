from ftw.tika.exceptions import ProcessError
from ftw.tika.utils import run_process
from ftw.tika.utils import strip_thumbnail_names
from ftw.tika.utils import strip_word_bookmarks
from unittest2 import TestCase


class TestUtils(TestCase):

    def test_run_process_returns_stdout_and_stderr(self):
        cmd = "echo stdout; echo stderr 1>&2"
        stdout, stderr = run_process(cmd)
        self.assertEquals(stdout, 'stdout\n')
        self.assertEquals(stderr, 'stderr\n')

    def test_run_process_raises_process_error_on_nonzero_exit_code(self):
        cmd = "false"
        with self.assertRaises(ProcessError):
            stdout, stderr = run_process(cmd)

    def test_strip_word_bookmarks_removes_bookmarks_from_docx(self):
        text = '[bookmark: Foo][bookmark: _GoBack]Lorem Ipsum[bookmark: Foo]'
        self.assertEquals(
            'Lorem Ipsum',
            strip_word_bookmarks(text, filename='foo.docx'))

    def test_strip_word_bookmarks_doesnt_touch_files_other_than_docx(self):
        text = '[bookmark: Foo][bookmark: _GoBack]Lorem Ipsum[bookmark: Foo]'
        self.assertEquals(text, strip_word_bookmarks(text))

    def test_strip_thumbnail_names_removes_thumbnail_filenames(self):
        text = 'Lorem Ipsum\nthumbnail_0.jpeg'
        self.assertEquals(
            'Lorem Ipsum',
            strip_thumbnail_names(text).strip())
