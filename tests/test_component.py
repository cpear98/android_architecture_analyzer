import unittest
from unittest.mock import Mock
import sys
sys.path.append('..')
from src.entities import Component, Interface


class TestComponent(unittest.TestCase):
    mock = Mock()

    def test_add_interface(self):
        component = Component()
        component.add_interface(self.mock)

        self.assertTrue(self.mock in component.get_interfaces())

    def test_remove_interface(self):
        component = Component()
        component.add_interface(self.mock)
        
        self.assertTrue(self.mock in component.get_interfaces())

        component.remove_interface(self.mock)

        self.assertFalse(self.mock in component.get_interfaces())

    def test_add_interface_out(self):
        component = Component()

        self.mock.get_direction = lambda: Interface.DIRECTION_OUT
        component.add_interface_out(self.mock)

        self.assertTrue(self.mock in component.get_interfaces())
        self.assertTrue(self.mock is component.get_interface_out())
        self.mock.get_direction = None

    def test_add_interface_in(self):
        component = Component()

        self.mock.get_direction = lambda: Interface.DIRECTION_IN
        component.add_interface_in(self.mock)

        self.assertTrue(self.mock in component.get_interfaces())
        self.assertTrue(self.mock is component.get_interface_in())
        self.mock.get_direction = None

if __name__ == '__main__':
    unittest.main()