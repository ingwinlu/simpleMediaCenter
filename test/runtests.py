import sys
import os
import logging
import unittest

#logging.basicConfig(level=logging.DEBUG)

sys.path.insert(0, os.path.abspath("../"))

testsuite = unittest.TestLoader().discover(start_dir='.', pattern='Test*.py')
runner=unittest.TextTestRunner(verbosity=2).run(testsuite)
