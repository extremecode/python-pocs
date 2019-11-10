import os
import shutil
import stat
import tempfile
from unittest import TestCase
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class IntegrationTestSupport(TestCase):
    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp(prefix="IntegrationTestSupport")

    def tearDown(self):
        outcomes = self.outcomes()
        if self.tmp_directory and os.path.exists(self.tmp_directory) and not (outcomes[0] or outcomes[1]):
            shutil.rmtree(self.tmp_directory)

    def full_path(self, name):
        parts = [self.tmp_directory] + name.split(os.sep)
        return os.path.join(*parts)

    def create_directory(self, name):
        os.makedirs(self.full_path(name))

    def write_file(self, name, *content):
        with open(self.full_path(name), "w") as file:
            file.writelines(content)

    def write_binary_file(self, name, *content):
        with open(self.full_path(name), "wb") as file:
            file.writelines(content)

    def write_build_file(self, content):
        self.write_file("build.py", content)

    def assert_directory_exists(self, name):
        full_path = self.full_path(name)
        self.assertTrue(os.path.exists(full_path), msg="Directory does not exist: %s" % full_path)
        self.assertTrue(os.path.isdir(full_path), msg="Not a directory: %s" % full_path)

    def assert_file_does_not_exist(self, name):
        full_path = self.full_path(name)
        self.assertFalse(os.path.exists(full_path), msg="File should NOT exist: %s" % full_path)

    def assert_file_exists(self, name):
        full_path = self.full_path(name)
        self.assertTrue(os.path.exists(full_path), msg="File does not exist: %s" % full_path)
        self.assertTrue(os.path.isfile(full_path), msg="Not a file: %s" % full_path)

    def assert_file_permissions(self, expected_permissions, name):
        full_path = self.full_path(name)
        actual_file_permissions = stat.S_IMODE(os.stat(full_path).st_mode)
        if sys.platform != "win32":
            self.assertEqual(oct(expected_permissions), oct(actual_file_permissions))
        else:
            self.assertEqual(oct(0o666), oct(actual_file_permissions))

    def assert_file_empty(self, name):
        self.assert_file_exists(name)
        full_path = self.full_path(name)
        self.assertEqual(0, os.path.getsize(full_path), msg="File %s is not empty." % full_path)

    def assert_file_contains(self, name, expected_content_part):
        full_path = self.full_path(name)
        with open(full_path) as file:
            content = file.read()
            self.assertTrue(expected_content_part in content)

    def assert_file_content(self, name, expected_file_content):
        if expected_file_content == "":
            self.assert_file_empty(name)

        count_of_new_lines = expected_file_content.count("\n")

        if count_of_new_lines == 0:
            expected_lines = 1
        else:
            expected_lines = count_of_new_lines

        expected_content = StringIO(expected_file_content)
        actual_line_number = 0

        full_path = self.full_path(name)
        with open(full_path) as file:
            for actual_line in file:
                actual_line_number += 1
                actual_line_showing_escaped_new_line = actual_line.replace("\n", "\\n")

                expected_line = expected_content.readline()
                expected_line_showing_escaped_new_line = expected_line.replace("\n", "\\n")

                message = 'line {0} is not as expected.\n   expected: "{1}"\n    but got: "{2}"'.format(
                    actual_line_number, expected_line_showing_escaped_new_line, actual_line_showing_escaped_new_line)
                self.assertEqual(expected_line, actual_line, message)

        self.assertEqual(expected_lines, actual_line_number)

    def outcomes(self):
        result = self._get_result()
        return self._list2reason(result.errors), self._list2reason(result.failures)

    def _get_result(self):
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        return result

    def _list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
