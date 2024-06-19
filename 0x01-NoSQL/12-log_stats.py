#!/usr/bin/env python3
"""a Python script that provides some stats
about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def count_nginx_logs(mongo_collection):
    """provides some stats about Nginx logs in mongoDB"""
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        query = {"method": method}
        count = mongo_collection.count_documents(query)
        print(f"\tmethod {method}: {count}")

    status_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_count} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    count_nginx_logs(db.nginx)
