#!/usr/bin/env python3
"""
Module 9-insert_school.py: insert a document in python
"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    '''
    inserts new document based on kwargs
    mongo_collection will be the pymongo object
    returns the new _id
    '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
