"""
ShopEasy - Main Application Entry Point
Lab 1: Amazon EBS - Persistent Block Storage
"""

import argparse
from shopeasy import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", help="Database connection string", default=None)
    args = parser.parse_args()

    app = create_app(db_uri=args.dbpath)
    app.run(host="0.0.0.0", port=5000, debug=False)
