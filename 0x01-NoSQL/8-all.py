#!/usr/bin/env python3
"""lists all documents in a collection"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
