import sys
import os
import logging
import unittest

sys.path.insert(0, os.path.abspath("../simpleMediaCenter/"))

testsuite = unittest.TestLoader().discover(start_dir='.', pattern='Test*.py')
runner=unittest.TextTestRunner(verbosity=2).run(testsuite)
