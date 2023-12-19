#!/usr/bin/env python3
'''
Module 101-students.py: returns all students sorted by avg score
'''
from pymongo import MongoClient


def top_students(mongo_collection):
    '''
    func that returns all students sorted by average score
    mongo_collection: pymongo object
    ordered, avg score must be part of each item returns with
    key = averageScore
    '''
    pipeline = [
            {
                '$project': {
                    'name': '$name',
                    'averageScore': {'$avg': '$topics.score'}
                }
            },
            {
                '$sort': {
                    'averageScore': -1
                }
            }
    ]
    return mongo_collection.aggregate(pipeline)
