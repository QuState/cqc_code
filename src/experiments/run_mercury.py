#!/usr/bin/env python
import os
import sys

from mercury.mercury import main

if __name__ == '__main__':
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + os.pathsep + SRC_DIR
    sys.argv.append('run')
    sys.exit(main())
