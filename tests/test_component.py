import unittest
from unittest.mock import Mock
import sys
sys.path.append('..')
from src.entities import Component


class TestComponent(unittest.TestCase):
    mock = Mock()

    def test_add_interface(self):
        component = Component()
        component.add_interface(mock)

        self.assertEqual(component.get_interfaces()[0], mock)

    def test_get_interfaces(self):
        pass

    def test_remove_interface(self):
        pass

    def test_get_interface_out(self):
        pass

    def test_add_interface_out(self):
        pass

    def test_add_interface_in(self):
        pass

    def test_to_xml(self):
        pass

if __name__ == '__main__':
    unittest.main()