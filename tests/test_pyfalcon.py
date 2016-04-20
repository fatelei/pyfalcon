# -*- coding: utf8 -*-
"""
tests.test_pyfalcon.

~~~~~~~~~~~~~~~~~~~~

Pyfalcon unittests.
"""

import time
import unittest

from pyfalcon.client import Client


class TestPyFalcon(unittest.TestCase):
    """Pyfalcon unittests."""

    def setUp(self):
        """Setup some environment for per test."""
        self.c = Client(host="localhost")

    def test_format_content(self):
        """Test method `_format_content`."""
        payload = self.c._format_content("test", 1, "GAUGE", "")
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

    def test_get_buffer(self):
        """Test method `_get_buffer`."""
        c = Client(step=10)
        payload = c._format_content("test", 1, "GAUGE", "")
        rst = c._get_buffer(payload)
        self.assertTrue(rst is None)

        time.sleep(10)
        rst = c._get_buffer(payload)
        self.assertTrue(rst is not None)
