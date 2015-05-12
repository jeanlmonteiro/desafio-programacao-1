#! /usr/bin/env python
import unittest


suite = unittest.TestLoader().discover('', pattern='*_test.py')

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
