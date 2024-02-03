import unittest
from unittest.mock import patch
from curses import wrapper

@patch('curses_tests.control-loop-curses.phone_connected', True)