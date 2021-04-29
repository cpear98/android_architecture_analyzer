import unittest
from unittest.mock import Mock
import sys
sys.path.append('..')
from src.entities import Document, Connector, Component, Link

class TestDocument(unittest.TestCase):
    mock = Mock

    def test_add_remove_bus(self):
        doc = Document("test.xml", "test-struct")

        doc.add_bus()

        self.assertTrue(doc.get_bus() is not None)
        self.assertTrue(type(doc.get_bus()) is Connector)

        doc.remove_bus()

        self.assertTrue(doc.get_bus() is None)
    
    def test_add_component(self):
        doc = Document("test.xml", "test-struct")
        
        doc.add_component(self.mock)

        self.assertTrue(self.mock in doc.get_components())
    
    def test_add_connector(self):
        doc = Document("test.xml", "test-struct")
        
        doc.add_connector(self.mock)

        self.assertTrue(self.mock in doc.get_connectors())
        
    def test_add_remove_link_with_link(self):
        doc = Document("test.xml", "test-struct")
        
        sender = Component()
        receiver = Component()

        doc.add_component(sender)
        doc.add_component(receiver)

        link = doc.add_link(sender, receiver)

        self.assertTrue(link in doc.get_links())

        doc.remove_link(link)

        self.assertFalse(link in doc.get_links())

    #@unittest.skip
    def test_add_remove_link_with_endpoints(self):
        doc = Document("test.xml", "test-struct")
        
        sender = Component()
        receiver = Component()

        doc.add_component(sender)
        doc.add_component(receiver)

        link = doc.add_link(sender, receiver)

        self.assertTrue(link in doc.get_links())

        doc.remove_link(start=sender, end=receiver)

        self.assertFalse(link in doc.get_links())
        
    def test_get_link(self):
        doc = Document("test.xml", "test-struct")

        sender = Component()
        receiver = Component()

        link = doc.add_link(sender, receiver)

        self.assertTrue(doc.get_link(sender, receiver) is link)