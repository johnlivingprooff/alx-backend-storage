#!/usr/bin/env python3
"""log stats from the collection stats"""
from pymongo import MongoClient


def check_stats():
    """check the stats"""
    client = MongoClient()
    db = client.logs.nginx

    count = db.count_documents({})
    print(f"{count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    for method in methods:
        m_count = db.count_documents({"method": method})
        print(f"\tmethod {method}: {m_count}")
    stat_count = db.count_documents({"method": "GET", "path": "/status"})

    print(f"{stat_count} status check")

if __name__ == "__main__":
    check_stats()
