#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 09:02:43 2018

@author: thomas
"""

"""
create database from csv files
if database already exist, tables are deleted before being created
"""

import sqlite3
import pandas as pd  

def db_sql_create_table(db_name,QUERY):
    """create table with QUERY in db_name. Nothing is returned"""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(QUERY)
    conn.commit()
    conn.close()
    
def db_sql_insert_data(db_name,table_name,csv_file):
    """insert csv_file data in db_name / table_name. Nothing is returned"""
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_name)
    conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

def create_database(db_name):
    try:
        print 'NODE table is removed from', db_name
        QUERY='''DROP TABLE NODE'''
        db_sql_create_table(db_name,QUERY)
    except:
        print 'NODE table does not exist'
    
    QUERY='''CREATE TABLE NODE
    (
        id INTEGER PRIMARY KEY,
        lat REAL,
        lon REAL,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
    )'''
    print 'NODE table is created with following schema' 
    print QUERY
    db_sql_create_table(db_name,QUERY)
    
    print 'Data from nodes.csv are inserted inside NODE table '
    db_sql_insert_data(db_name,'NODE','nodes.csv')
    
    try:
        print 'NODE_TAG table is removed from', db_name
        QUERY='''DROP TABLE NODE_TAG'''
        db_sql_create_table(db_name,QUERY)
    except:
        print 'NODE_TAG table does not exist'
    
    QUERY='''CREATE TABLE NODE_TAG
    (
        id INTEGER,
        key TEXT,
        value TEXT,
        type TEXT,
        FOREIGN KEY (id) REFERENCES NODE (id)
    )'''
    print 'NODE_TAG table is created with following schema' 
    print QUERY
    db_sql_create_table(db_name,QUERY)
    
    print 'Data from nodes_tags.csv are inserted inside NODE_TAG table '
    db_sql_insert_data(db_name,'NODE_TAG','nodes_tags.csv')
    
    
    try:
        print 'WAY table is removed from', db_name
        QUERY='''DROP TABLE WAY'''
        db_sql_create_table(db_name,QUERY)
    except:
        print 'WAY table does not exist'
    
    QUERY='''CREATE TABLE WAY
    (
        id INTEGER PRIMARY KEY,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
    )'''
    print 'WAY table is created with following schema' 
    print QUERY
    db_sql_create_table(db_name,QUERY)
    
    print 'Data from ways.csv are inserted inside WAY table '
    db_sql_insert_data(db_name,'WAY','ways.csv')
    
    
    try:
        print 'WAY_TAG table is removed from', db_name
        QUERY='''DROP TABLE WAY_TAG'''
        db_sql_create_table(db_name,QUERY)
    except:
        print 'WAY_TAG table does not exist'
    
    QUERY='''CREATE TABLE WAY_TAG
    (
        id INTEGER,
        key TEXT,
        value TEXT,
        type TEXT,
        FOREIGN KEY (id) REFERENCES WAY (id)
    )'''
    print 'WAY_TAG table is created with following schema' 
    print QUERY
    db_sql_create_table(db_name,QUERY)
    
    print 'Data from ways_tags.csv are inserted inside WAY_TAG table '
    db_sql_insert_data(db_name,'WAY_TAG','ways_tags.csv')
    
    
    try:
        print 'WAY_NODES table is removed from', db_name
        QUERY='''DROP TABLE WAY_NODES'''
        db_sql_create_table(db_name,QUERY)
    except:
        print 'WAY_NODES table does not exist'
    
    QUERY='''CREATE TABLE WAY_NODES
    (
        id INTEGER,
        node_id INTEGER,
        position INTEGER,
        FOREIGN KEY (id) REFERENCES WAY (id),
        FOREIGN KEY (node_id) REFERENCES NODE (id)
    )'''
    print 'WAY_NODES table is created with following schema' 
    print QUERY
    db_sql_create_table(db_name,QUERY)
    
    print 'Data from ways_nodes.csv are inserted inside WAY_NODES table '
    db_sql_insert_data(db_name,'WAY_NODES','ways_nodes.csv')


if __name__ == '__main__':
    db_name='Toulouse_osm.db'
    create_database(db_name)
