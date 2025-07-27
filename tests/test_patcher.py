# tests/test_patcher.py

import unittest
from flexipatch import RobustPatcher

class TestRobustPatcher(unittest.TestCase):

    def setUp(self):
        self.patcher = RobustPatcher()

    def test_simple_addition(self):
        original = "hello\nworld\n"
        patch = """--- a/file.txt
+++ b/file.txt
@@ -1,2 +1,3 @@
 hello
+beautiful
 world
"""
        expected = "hello\nbeautiful\nworld\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_simple_deletion(self):
        original = "hello\nbeautiful\nworld\n"
        patch = """--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,2 @@
 hello
-beautiful
 world
"""
        expected = "hello\nworld\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_simple_modification(self):
        original = "this is a test\n"
        patch = """--- a/file.txt
+++ b/file.txt
@@ -1,1 +1,1 @@
-this is a test
+this was a test
"""
        expected = "this was a test\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_forgiving_whitespace_in_context(self):
        original = "def my_func():\n    print('hello')\n"
        # Patch has different indentation for the context line
        patch = """--- a/file.py
+++ b/file.py
@@ -1,2 +1,3 @@
 def my_func():
+    # A new comment
   print('hello')
"""
        expected = "def my_func():\n    # A new comment\n    print('hello')\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_forgiving_line_endings(self):
        original = "line one\r\nline two\r\n"
        patch = "@@ -1,2 +1,3 @@\n line one\n+line one-point-five\n line two\n"
        expected = "line one\nline one-point-five\nline two\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_multiple_hunks(self):
        original = "one\ntwo\nthree\nfour\nfive\nsix\n"
        patch = """--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,3 @@
 one
-two
+2
 three
@@ -4,3 +4,3 @@
 four
-five
+5
 six
"""
        expected = "one\n2\nthree\nfour\n5\nsix\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_context_mismatch_fails(self):
        original = "hello\nworld\n"
        patch = """--- a/file.txt
+++ b/file.txt
@@ -1,2 +1,3 @@
 hello
+extra
 universe
"""
        with self.assertRaises(ValueError):
            self.patcher.apply_patch(original, patch)

    def test_no_newline_at_end_of_file(self):
        original = "first\nsecond"
        patch = """--- a/file.txt
+++ b/file.txt
@@ -1,2 +1,2 @@
 first
-second
+the end
\\ No newline at end of file
"""
        expected = "first\nthe end"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)

    def test_adding_to_empty_file(self):
        original = ""
        patch = """--- /dev/null
+++ b/new_file.txt
@@ -0,0 +1,3 @@
+line 1
+line 2
+line 3
"""
        expected = "line 1\nline 2\nline 3\n"
        self.assertEqual(self.patcher.apply_patch(original, patch), expected)


if __name__ == '__main__':
    unittest.main()