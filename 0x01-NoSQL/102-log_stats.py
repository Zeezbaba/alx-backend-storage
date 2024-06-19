#!/usr/bin/env python3
"""a Python script that provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def count_nginx_logs(mongo_collection):
    """provide stats about Nginx logs stored in MongoDB"""
    print('{} logs'.format(mongo_collection.count_documents({})))

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        query = { "method": method }
        count = mongo_collection.count_documents(query)
        print(f"\tmethod {method}: {count}")

    status_count = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_count} status check")


    print("IPs:")
    ipsList = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(ipsList)
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    count_nginx_logs(mongo_collection)
