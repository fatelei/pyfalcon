# -*- coding: utf8 -*-
"""
pyfalcon.client.

~~~~~~~~~~~~~~~~

HTTP Client.
"""

import functools
import logging
import json
import socket
import time
import requests

from requests.exceptions import Timeout
from tornado.httpclient import AsyncHTTPClient

from pyfalcon.macro import CounterType

logger = logging.getLogger(__name__)


class Timer(object):
    """Timer."""

    def __init__(self, client, metric, step=60, tags=None):
        """Initialize.

        :param object client: An instance of `pyfalcon.client.Client`
        :param str metric: The name of metric
        :param int step: The cycle of report
        :param str tags: Tags
        """
        self.client = client
        self.metric = metric
        self.step = step
        self.tags = self.client._format_tags(tags)
        self.payload = self.client._format_content(
            self.metric, -1, self.step, CounterType.GAUGE, self.tags)

    def __call__(self, func):
        """Override `__call__`."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                rst = func(*args, **kwargs)
            finally:
                elapse = (time.time() - start) * 1000  # ms
                self.payload["value"] = elapse
                self.client._send(self.payload)
            return rst
        return wrapper

    def __enter__(self):
        """Enter the context."""
        self.start = time.time()

    def __exit__(self, typ, value, tb):
        """Leave the context."""
        elapse = (time.time() - self.start) * 1000  # ms
        self.payload["value"] = elapse
        self.client._send(self.payload)


class Client(object):
    """HTTP client."""

    def __init__(self, host=None, port=1988, timeout=1):
        """Initialize.

        :param str host: Open falcon agent host, ip or hostname
        :param int port: Open falcon agent port
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.endpoint = socket.gethostname()
        self.push_api = "http://{}:{}/v1/push".format(self.host, self.port)

    def _send(self, payload):
        """Send data to open falcon agent.

        :param dict data: Metric data
        """
        if isinstance(payload, dict):
            payload = json.dumps([payload])

            try:
                requests.post(
                    self.push_api, data=payload, timeout=self.timeout)
            except (Timeout, RuntimeError):
                pass

    def _format_tags(self, tags_dict):
        """Convert the format of tags to open falcon's requirement.

        :param dict tags_dict: Tags dict
        :return: A tag str.
        """
        if not isinstance(tags_dict, dict):
            return ""

        tmp = map(lambda x: "{}={}".format(x[0], x[1]), tags_dict.items())
        return ",".join(tmp)

    def _format_content(self, metric, value, step, counter_type, tags):
        """Generate data to meet with the requirement of open falcon.

        :param str metric: The name of metric
        :param float/int value: The current time of the value of the metric
        :param int step: The cycle of report
        :param str counter_type: The type of counter
        :param str tags: Tags
        """
        payload = {
            "endpoint": self.endpoint,
            "metric": metric,
            "timestamp": int(time.time()),
            "step": step,
            "value": value,
            "counterType": counter_type,
            "tags": tags
        }
        return payload

    def gauge(self, metric, value, step=60, tags=None):
        """Collect metric using the type of counter.

        :param str metric: The name of metric, required
        :param float/int value: Metric value
        :param int step: The cycle of report, default is 60s, optional
        :param dict tags: Tags, optional
        """
        tags = self._format_tags(tags)
        payload = self._format_content(
            metric, value, step, CounterType.GAUGE, tags)

        self._send(payload)

    def timer(self, metric, step=60, tags=None):
        """Timer used to record response time.

        :param str metric: The name of metric
        :param int step: The cycle of report, default is 60s, optional
        :param dict tags: Tags, optional
        :return: An instance of `pyfalcon.client.Timer`.
        """
        return Timer(self, metric, step, tags)


class AsyncClient(Client):
    """Async client."""

    def _finish(self, response):
        """Finish callback."""
        if response.error:
            logger.error(response.error)
        else:
            logger.debug(response.body)

    def _send(self, payload):
        """Send data to open falcon agent.

        :param dict data: Metric data
        """
        if isinstance(payload, dict):
            payload = json.dumps([payload])

            http_client = AsyncHTTPClient()
            http_client.fetch(self.push_api,
                              method="POST",
                              body=payload,
                              connect_timeout=self.timeout,
                              request_timeout=self.timeout,
                              callback=self._finish)
