#!/usr/bin/env python3
'''
Module 10-update_topics.py: changes all topics of a school document
based on name
'''
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    '''
    function that changes all topics of a school document based on names
    mongo_collection: pymongo obj
    name: school name to update
    topic: list of topics approached in the school
    '''
    update = mongo_collection.update_one(
            {'name': name},
            {'$set': {'topics': topics}}
            )
    return update
