import os, sys
import gc
import math
import time
from collections import defaultdict, Counter
import pandas as pd
import numpy as np
from sklearn import preprocessing
from data import *
import constant


"""
Utils
"""
TESTPATHS = [
    (1610, constant.FEATURE_FACTORY_TEST_1610),
    (1611, constant.FEATURE_FACTORY_TEST_1611),
    (1612, constant.FEATURE_FACTORY_TEST_1612),
    (1710, constant.FEATURE_FACTORY_TEST_1710),
    (1711, constant.FEATURE_FACTORY_TEST_1711),
    (1712, constant.FEATURE_FACTORY_TEST_1712)
]
