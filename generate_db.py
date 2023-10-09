import argparse
import datetime
import pandas as pd
import random
import sqlite3 as sl
import sys

class TxnGenerator():
    """
    Generate a given number of users and transactions. Transaction properties are randomally determined.
    At the same time as the internal details are generated, a third party record is generated to represent
    the third part reconciliation records.
    """
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def generate(self, num_users, num_txns):
        # Generate num_users users.
        user_ids = []
        user_types = []
        for i in range(num_users):
            user_ids.append(i)
            user_types.append(random.choices([0, 1], weights=[3, 1])[0])
        df_users = pd.DataFrame({"id": user_ids, "type": user_types}).set_index("id")
        df_users.to_sql("users", self.db_conn)

        # Generate num_txns transactions, starting from the beginning of 2022.
        txn_id = 0
        timestamp = datetime.datetime(2022, 1, 1, 0, 0, 0)
        txn_ids = []
        txn_created_at = []
        txn_products = []
        txn_amounts = []
        txn_statuses = []
        txn_user_ids = []
        txn_completed_at = []
        tp_ids = []
        tp_amounts = []
        tp_timestamps = []
        tp_products = []
        while txn_id < num_txns:
            # Every ten seconds, 50/50 create a transaction or do nothing.
            action = random.choices(["skip", "txn"], weights=[1, 1])[0]
            if action == "txn":
                txn_ids.append(txn_id)
                txn_created_at.append(timestamp)
                txn_products.append(random.choices(["ProdA", "ProdB"], weights=[3, 5])[0])
                txn_amounts.append(max(0.01, round(random.normalvariate(20, 10), 2)))
                # Most txns succeed, some fail, a few get stuck in PENDING.
                txn_statuses.append(random.choices(["SUCCESS", "FAILURE", "PENDING"], weights=[1000, 20, 2])[0])
                txn_user_ids.append(random.choice(range(num_users)))
                # Transactions normally settle within a few seconds, but can take longer. Cap at 3 days.
                txn_completed_at.append(timestamp + datetime.timedelta(seconds=min(random.lognormvariate(3,10), 72*60*60)))
                # Rarely the third parties just don't record the transaction.
                tp_action = random.choices(["skip", "txn"], weights=[1, 2000])[0]
                if tp_action == "txn" and txn_statuses[-1] != "FAILURE":
                    # Note failed transactions are not recorded. Some transactions are reported in recon, but
                    # FFI think are stuck pending.
                    tp_ids.append(txn_id)
                    # Rarely the third parties are out by a penny/cent.
                    tp_amounts.append(txn_amounts[-1] + random.choices([-0.01, 0, 0.01], weights=[1, 2000, 1])[0])
                    # Third party settlement timestamps are ususally around when FFI thinks the txn completed. But with some variance.
                    tp_timestamps.append(txn_completed_at[-1] + datetime.timedelta(seconds=random.normalvariate(0,180)))
                    tp_products.append(txn_products[-1])
                txn_id += 1
            timestamp += datetime.timedelta(seconds=10)

        # Write the FFI transaction records to the DB.
        df_txns = pd.DataFrame({"id": txn_ids, "created_at": txn_created_at, "product": txn_products, "amount": txn_amounts, "status": txn_statuses, "user_id": txn_user_ids, "completed_at":  txn_completed_at}).set_index("id")
        df_txns.to_sql("transactions", self.db_conn)

        # Split the third party recon records by product, then write to their respective DB tables.
        df_tp_txns = pd.DataFrame({"id": tp_ids, "amount": tp_amounts, "timestamp": tp_timestamps, "product": tp_products}).set_index("id")
        df_tpa_txns = df_tp_txns[df_tp_txns["product"] == "ProdA"].drop(columns=["product"])
        df_tpb_txns = df_tp_txns[df_tp_txns["product"] == "ProdB"].drop(columns=["product"])
        df_tpa_txns.to_sql("tpa_recon", self.db_conn)
        df_tpb_txns.to_sql("tpb_recon", self.db_conn)

    def report(self):
        # Query the transactions table to give some overall stats.
        report_df = pd.read_sql("SELECT MIN(created_at) AS start, MAX(created_at) AS end, COUNT(*) AS count FROM transactions", self.db_conn)
        print(f"Generated {report_df.at[0, 'count']} transactions from {report_df.at[0, 'start']} to {report_df.at[0, 'end']}.")

def main():
    random.seed(2022) # Aid repeatability

    parser = argparse.ArgumentParser()
    parser.add_argument("num_users", type=int, help="Number of users to generate")
    parser.add_argument("num_txns", type=int, help="Number of users to generate")
    args = parser.parse_args()

    db_conn = sl.connect("generated_txns.db")
    gen = TxnGenerator(db_conn)
    gen.generate(args.num_users, args.num_txns)
    gen.report()

if __name__ == "__main__":
    sys.exit(main())
