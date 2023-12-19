#!/usr/bin/env python3
'''
Module 8-all: Modules that lists all documents in a collection
'''

from pymongo import MongoClient


def list_all(mongo_collection):
    '''
    python func that lists all documents in a collection
    returns an empty list if no document in the collection
    '''
    cursor = mongo_collection.find({})
    documents = list(cursor)
    return documents
