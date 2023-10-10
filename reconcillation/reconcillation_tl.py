import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

# setting path
from plugins.sql_harness import SqlHarness

# Configuration 

MODULE_NAME = "reconcillation"
FILENAME = "reconcillation_config.yaml"

# initialize Sql class with provided config and module
reconcillation = SqlHarness(filename=FILENAME, module=MODULE_NAME)

# generate all reports
reconcillation.generate_all_reports()