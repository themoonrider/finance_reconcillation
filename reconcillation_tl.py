from sql_harness import SqlHarness


# Configuration 

MODULE_NAME = "reconcillation"
FILENAME = "reconcillation_config.yaml"

# initialize Sql class with provided config and module
reconcillation = SqlHarness(filename=FILENAME, module=MODULE_NAME)

# generate all reports
reconcillation.generate_all_reports()