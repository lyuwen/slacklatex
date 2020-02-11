#!/usr/bin/env python3
import os
import sys
basepath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basepath)

from main import app as application
