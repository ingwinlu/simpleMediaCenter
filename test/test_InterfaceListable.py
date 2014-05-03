from simpleMediaCenter.interface.Interface import InterfaceListable
import unittest
import time
import requests

class TestInterfaceListable(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_creation_1(self):
        with self.assertRaises(TypeError):
            InterfaceListable(None)
    '''    
    it is now allowed to create an empty InterfaceListable
    def test_creation_2(self):
        with self.assertRaises(TypeError):
            InterfaceListable([])
    '''        
    def test_set_outofbounds_1(self):
        with self.assertRaises(TypeError):
            interfaceListable=InterfaceListable(['a','b','c'])
            interfaceListable.setActive(-1)
            
    def test_set_outofbounds_2(self):
        with self.assertRaises(TypeError):
            interfaceListable=InterfaceListable(['a','b','c'])
            interfaceListable.setActive(3)
            
    def test_getActive(self):
        interfaceListable=InterfaceListable(['a','b','c'])
        self.assertEqual(interfaceListable.getActive(), 'a')
        
    def test_setActive(self):
        interfaceListable=InterfaceListable(['a','b','c'])
        interfaceListable.setActive(1)
        self.assertEqual(interfaceListable.getActive(), 'b')
      
    '''
    def test_getArray(self):
        array = ['a','b','c']
        interfaceListable=InterfaceListable(array)
        self.assertEqual(array, interfaceListable.getArray())
    '''
       
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestInterfaceListable))
        return testSuite
        
