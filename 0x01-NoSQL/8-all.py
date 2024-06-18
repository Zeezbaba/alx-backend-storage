#!/usr/bin/env python3
"""a Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """returns list of all doc."""
    return [doc for doc in mongo_collection.find()]
