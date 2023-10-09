import yaml
import logging
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta 
logging.basicConfig(level=logging.INFO)

class SqlHarness():
    def __init__(self, filename="", module=""):
        self.filename = filename
        self.module = module
        self.config_vals = self._get_config_vals()

    def _get_config_vals(self):
        if not self.filename.endswith(".yaml"):
            raise SystemExit(1)
        
        with open(self.module + "/config/" + self.filename) as read_file:
            content = yaml.safe_load(read_file)
        if 'start_date' not in content or 'end_date' not in content:
            raise KeyError("config file missing date range parameters")
        return content

    def _get_query(self, sql_file, ** param):
        sql_file_path = os.path.join(os.path.normpath(self.module), 'stage_logic/', sql_file)
        with open(sql_file_path, 'r') as file:
            sql_str = file.read()
            query = sql_str.format(**param)
        file.close()
        return query

    # create a date table for management summary report
    def _create_date_table(self, conn):
        df = pd.DataFrame(pd.date_range(start='2022-01-01',
                           end=datetime.strftime(datetime.now(), "%Y-%m-%d"), freq='D'),
                           columns=['date']
                        )
        
        df.to_sql("date_range", conn, if_exists='replace')

    
    def _build_executor(self, sql_params, entity_row, conn):
        source_table_id = entity_row.get("source_table_id", "")   
        start_date = entity_row.get("start_date", self.config_vals['start_date'])
        end_date = entity_row.get("end_date", self.config_vals['end_date'])
        
        # if manangement report, date range for the report is 30 days ago from today.
        if entity_row['sql_logic'] == 'management_summary':
            start_date = datetime.strftime(datetime.now() - timedelta(days=30), "%Y-%m-%d")
            end_date = datetime.strftime(datetime.now(), "%Y-%m-%d")

        filter = entity_row.get("filter", "")
        sql_params.update({
            "start_date": start_date,
            "end_date": end_date, 
            "source_table_id": source_table_id,
            "filter": filter
        })

        sql_file = f"{entity_row['sql_logic']}.sql"
        query = self._get_query(sql_file,**sql_params)

        # Run query
    
        df = pd.read_sql_query(query, conn)

        # Write to csv file    
        report_name = f"{entity_row['name']}_{start_date}_{end_date}.csv"
        destination_dir = os.path.join(os.path.normpath(self.module), 'reports/')
        
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        destination_report = os.path.join(destination_dir, report_name)
        df.to_csv(destination_report, index=False)
       
        logging.info(f"report {destination_report} exported")

    
    
    def generate_all_reports(self):
        entity = self.config_vals['entity']
        db_name = f"{self.config_vals['database_name']}.db"
        sql_params =self.config_vals['sql_params']

        try:
            conn = sqlite3.connect(db_name)
            # Create date range table for management_summary    
            self._create_date_table(conn)
                
            for entity_row in entity:
                self._build_executor(sql_params, entity_row, conn)
        except sqlite3.Error as error:
            print(f"{error}")
        finally:
            conn.close()



        



        
        
   

    

    



