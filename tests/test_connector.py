import unittest
from unittest.mock import Mock
import sys
sys.path.append('..')
from src.entities import Connector


class TestConnector(unittest.TestCase):
    mock = Mock()
    
    def test_add_interface_out(self):
        connector = Connector()

        self.mock.get_direction = lambda: Interface.DIRECTION_OUT
        connector.add_interface_out(self.mock)

        self.assertTrue(self.mock is connector.get_interface_out())
        self.mock.get_direction = None

    def test_add_interface_in(self):
        connector = Connector()

        self.mock.get_direction = lambda: Interface.DIRECTION_IN
        connector.add_interface_in(self.mock)

        self.assertTrue(self.mock is connector.get_interface_in())
        self.mock.get_direction = None