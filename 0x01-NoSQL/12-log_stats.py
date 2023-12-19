#!/usr/bin/env python3
'''
Module 12-log_stats.py: script that provides some stats
stored in MongoDB
'''
from pymongo import MongoClient


def log_stats():
    '''
    function that logs stats of db stored in MongoDB
    '''
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    print(f'{total_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')

    status_path_count = collection.count_documents(
            {'method': "GET", 'path': '/status'}
            )
    print(f'{status_path_count} status check')


if __name__ == '__main__':
    log_stats()
