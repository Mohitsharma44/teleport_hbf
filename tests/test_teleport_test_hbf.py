#!/usr/bin/env python

"""Tests for `teleport_test_hbf` package."""


import unittest
import subprocess
import requests
import time
from click.testing import CliRunner

from teleport_test_hbf import teleport_test_hbf
from teleport_test_hbf import cli


class TestTeleport_test_hbf(unittest.TestCase):
    """Tests for `teleport_test_hbf` package."""

    def setUp(self):
        """
        Start multiple httpd container on different ports
        """
        for i in range(1, 9):
            subprocess.call(f'docker run -d --name web{i} -p 810{i}:80 httpd > /dev/null 2>&1', shell=True)

    def tearDown(self):
        """
        Tear down all web containers
        """
        for i in range(1, 9):
            subprocess.call(f'docker rm -f web{i} > /dev/null 2>&1', shell=True)

    def test_portScan(self):
        """
        Test portScan
        """
        for i in range(1, 9):
            resp = requests.get(f"http://localhost:810{i}", timeout=0.5)
            if i%6 == 0:
                print("Status Code: ", resp.status_code)
                assert resp.status_code != 200
            time.sleep(0.5)

    def test_command_line_interface(self):
        """Test the CLI"""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'HBF' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
