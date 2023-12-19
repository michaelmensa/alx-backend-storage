#!/usr/bin/env python3
'''
Module 11-schools_by_topic.py: list that returns the list of school
having a specific topic
'''
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    '''
    function that returns list of school having a specific topic
    mongo_collection: pymongo obj
    topic: topic to be searched
    Return: list of school having a specific topic
    '''
    return mongo_collection.find({"topics": topic})
