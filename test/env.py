import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UNIT_TEST_DIR = os.path.join(ROOT_DIR, "unit")
LIB_DIR = os.path.join(ROOT_DIR, "lib")
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, "acceptance")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
SRC_DIR = os.path.join(ROOT_DIR, "..", "src")

sys.path.insert(0, SRC_DIR)
sys.path.append(LIB_DIR)
sys.path.append(UNIT_TEST_DIR)
