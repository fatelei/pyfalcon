# -*- coding: utf8 -*-
"""
tests.test_pyfalcon.

~~~~~~~~~~~~~~~~~~~~

Pyfalcon unittests.
"""

import unittest


class TestPyFalcon(unittest.TestCase):
    """Pyfalcon unittests."""

    def setUp(self):
        """Setup some environment for per test."""
        from pyfalcon.client import Client
        self.c = Client(host="localhost")

    def test_format_content(self):
        """Test method `_format_content`."""
        payload = self.c._format_content("test", 1, 60, "GAUGE", "")
        self.assertIn("endpoint", payload)
        self.assertIn("metric", payload)
        self.assertIn("value", payload)
        self.assertIn("step", payload)
        self.assertIn("timestamp", payload)
        self.assertIn("counterType", payload)
        self.assertIn("tags", payload)

    def test_format_bad_tags(self):
        """Test method `_format_tags`, while tags is bad."""
        tags = self.c._format_tags(None)
        self.assertEqual(0, len(tags))

    def test_format_tags(self):
        """Test method `_format_tags`."""
        tags = self.c._format_tags({
            "idc": "lg",
            "loc": "beijing"
        })
        self.assertNotEqual(0, len(tags))
        self.assertIn("idc=lg", tags)
        self.assertIn("loc=beijing", tags)
