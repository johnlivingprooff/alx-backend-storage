#!/usr/bin/env python3
"""log stats from the collection stats"""
from pymongo import MongoClient


def check_stats():
    """check the stats"""
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db_C = client.logs.nginx

    # no of logs
    count = db_C.count_documents({})

    # method stat counts
    get = db_C.count_documents({"method": "GET"})
    post = db_C.count_documents({"method": "POST"})
    put = db_C.count_documents({"method": "PUT"})
    patch = db_C.count_documents({"method": "PATCH"})
    delete = db_C.count_documents({"method": "DELETE"})

    # no of GET request to /status
    stat_count = db_C.count_documents({"method": "GET", "path": "/status"})

    # printed stats
    print("{} logs".format(count))
    print("Methods:")
    print("    method GET: {}".format(get))
    print("    method POST: {}".format(post))
    print("    method PUT: {}".format(put))
    print("    method PATCH: {}".format(patch))
    print("    method DELETE: {}".format(delete))
    print("{} status check".format(stat_count))


if __name__ == "__main__":
    check_stats()
