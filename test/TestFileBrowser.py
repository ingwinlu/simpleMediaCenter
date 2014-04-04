from browser.Browser import FileBrowser
import unittest
import time
import os

class TestFileBrowser(unittest.TestCase):
    fileBrowser = None
    

    def setUp(self):
        self.fileBrowser = FileBrowser(".")
        
    def tearDown(self):
        self.fileBrowser = None
        
    def test_AbsPath(self):
        dic = self.fileBrowser.getDict()
        self.assertEqual(dic['browserWorkingDir'], os.path.abspath("."))
        
    def test_fileFind(self):
        dic = self.fileBrowser.getDict()
        self.assertEqual(dic['browserWorkingDir'], os.path.abspath("."))
        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestFileBrowser))
        return testSuite
        
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing FileCrawler")
    filecrawler = FileCrawler()
    logging.debug(filecrawler.getDirList())
    logging.debug(filecrawler.getFileList())
    logging.debug(filecrawler.getFileListPath(0))
    logging.debug(filecrawler.getDirListPath(0))