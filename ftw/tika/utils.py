"""Utility functions for ftw.tika.
"""

from ftw.tika.exceptions import ProcessError
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
