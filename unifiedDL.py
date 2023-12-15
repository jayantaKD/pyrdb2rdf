import os
import time
from argparse import ArgumentParser

import pymysql
import rdflib
import rdflib as _rdf
import sqlalchemy as _sqla
from pymongo import MongoClient
import mysql.connector
from rdflib import plugin
from sqlalchemy import text

from rdb2rdf.stores import DirectMapping


def RDF2RelationalParser():
    inputRdf = "F:\\UnifiedDL\\Resources\\Navigation data\\jsaf\\jsaf\\radar.n3"
    # inputRdf = "F:\\UnifiedDL\\Resources\\Navigation data\\jsaf\\jsaf\\runs.n3"
    baseIRI = 'http://orn.navy.mil/jsaf/'

    # g= _rdf.Graph()
    # g.parse(inputRdf)
    # print(len(g))

    # # open a database connection
    # # be sure to change the host IP address, username, password and database name to match your own
    # connection = pymysql.connect(host="192.168.1.136", user="vehchain", passwd="Inf0Bey0nd!", db="unifiedDLSource",
    #                              cursorclass=pymysql.cursors.DictCursor, ssl={"fake_flag_to_enable_tls": True})
    # # prepare a cursor object using cursor() method
    # cursor = connection.cursor()


    sqlList=[]
    with open(inputRdf) as f:
        count = 0
        commit_count = 0
        values = {}
        node=''
        tableName=''
        for line in f:
            # print 'printing -- ' + line
            splittedLine = line.strip().split(' ')
            # sql + columnString + dataString

            if splittedLine[0].strip() != node and node!='':
                sql = 'insert into unifiedDLSource.'+tableName
                columnString='('
                dataString=' values('
                index=1
                for key in values.keys():
                    if len(values.keys()) == index:
                        columnString = columnString + '`'+key+'`)'
                        dataString = dataString + values[key]+');'
                    else:
                        columnString = columnString + '`' + key + '`' + ','
                        dataString = dataString + values[key] + ','
                    index = index + 1
                    pass


                sqlList.append(sql + columnString + dataString) # save insert sql
                print (str(len(sqlList))+': ' + sql + columnString + dataString)
                values = {}

            node = splittedLine[0].strip()

            if splittedLine[1].strip() == '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>':
                text = splittedLine[2].strip().replace('<', '').replace('>', '').replace(baseIRI, '')
                tableName = text.strip().split(' ')[0].strip()
                # print tableName
            else:
                keyText = splittedLine[1].strip().replace('<', '').replace('>', '').replace(baseIRI, '').strip()
                keyValue = splittedLine[2].strip().replace('<', '').replace('>', '').replace('"', '').replace('^^', '').replace(baseIRI, '').strip()
                keyValue = keyValue.split('/')
                keyValue = keyValue[len(keyValue)-1]

                if keyText.startswith('has'):
                    keyText = keyText.replace('has', '')

                if keyValue.endswith('http://www.w3.org/2001/XMLSchema#double'):
                    values[keyText] = keyValue.replace('http://www.w3.org/2001/XMLSchema#double', '').strip()
                    pass
                else:
                    values[keyText] = '\''+keyValue+'\''
                    pass

                # print keyText
                # print keyValue

                pass


            # cursor.execute(sql)
            # print (splittedLine[1])

            commit_count=commit_count+1
            count=count+1
            # if commit_count == 50000:
            #     connection.commit()
            #     print(str(count) + " --------------> is committed")
            #     commit_count = 0

    # connection.commit()
    # cursor.close()
    pass

def JSONDatabase2RDF():
    connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
    client = MongoClient('localhost', 27017)
    db = client['UnifiedDLSource2']
    graph = _rdf.Graph('json2rdf_dm')
    graph.open(db)

    # with open('unifiedDLSourceTurtle1.n3', 'w') as f:
    #     f.write(graph.serialize(format='n3'))
    #     # f.write(graph.serialize(format='xml'))
    print ("W3C recommended drirect mapping algorithm converts UnifiedDL experimental JSON database \n(TargetDamageAssessments Object) into"
           " RDF (Resource Description Framework) graph data model(N-Triples Format):\n")
    print(graph.serialize(format='nt'))
    pass

def RelationalDatabase2RDF(connectionString, outputPath):
    # plugin.register('rdb2rdf_dm', rdflib.store.Store, './rdb2rdf', DirectMapping)
    connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
    db_str = 'mysql+pymysql://'+connectionString
    db = _sqla.create_engine(db_str, connect_args=connect_args)
    graph = _rdf.Graph('rdb2rdf_dm')
    graph.open(db)

    start = time.time()
    graph.serialize(format='n3')
    with open(outputPath, 'w') as f:
        # print 'executing'
        f.write(graph.serialize(format='n3'))
        # f.write(graph.serialize(format='xml'))
    # print ("W3C recommended drirect mapping algorithm converts UnifiedDL experimental Relational database \n(MilitaryEquipments Table) into"
    #        " RDF (Resource Description Framework) graph data model(N-Triples Format):\n")
    # print(graph.serialize(format='nt'))
    end = time.time()
    DirectMappingAlgorithmDuration = end - start
    print DirectMappingAlgorithmDuration
    graph.close()
    pass


def RelationalSchemaIngestion():
    connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
    db_str = 'mysql+pymysql://vehchain:Inf0Bey0nd!@192.168.1.136/unifiedDLSource1'
    db = _sqla.create_engine(db_str, connect_args=connect_args)

    sql = text('SHOW FULL TABLES')
    results = db.execute(sql)
    print('unifiedDLSource1 relational schema tables:')
    # View the records
    for record in results:
        print("\n", record)

    print('\nMilitaryEquipments table columns:')
    sql = text('DESCRIBE unifiedDLSource1.MilitaryEquipments')
    results = db.execute(sql)
    # View the records
    for record in results:
        print("\n", record)

    print('\nMunitionFireIncidents table columns:')
    sql = text('DESCRIBE unifiedDLSource1.MunitionFireIncidents')
    results = db.execute(sql)
    # View the records
    for record in results:
        print("\n", record)

    print('\nMunitionImpactIncidents table columns:')
    sql = text('DESCRIBE unifiedDLSource1.MunitionImpactIncidents')
    results = db.execute(sql)
    # View the records
    for record in results:
        print("\n", record)

    # # client = MongoClient()
    # client = MongoClient('localhost', 27017)
    # mydatabase  = client['UnifiedDLSource2']
    # print(mydatabase.command("collstats", "TargetDamageAssessments"))
    # mycollection = mydatabase['TargetDamageAssessments']
    # print(mycollection)
    # cursor = mycollection.find()
    # for record in cursor:
    #     print(record)
    # pass

def JSONSchemaIngestion():
    client = MongoClient('localhost', 27017)
    mydatabase  = client['UnifiedDLSource2']

    print ('ShooterToTargetMeters')
    print ('ShooterToDetonationMeters')
    print ('SlantRangeMeters')
    print ('PreDamageState')
    print ('ThisDamageResult')
    print ('NewDamageState')
    print ('DamageResultReason')
    print ('FirerVehicle')
    print ('FirerCourse')
    print ('FirerSpeedKnots')

    print ('unifiedDLSource2 JSON object collections:')
    print ('TargetDamageAssessments')
    print ('\nTargetDamageAssessments JSON object fields:')
    print ('id')
    print ('ZuluTime')
    print ('Timestamp')
    print ('DetonationResult')
    print ('Munition')
    print ('Target')
    print ('TargetCourse')
    print ('TargetSpeedKnots')
    print ('TargetFromDetonation')


    mydatabase.command("collstats", "TargetDamageAssessments")
    #
    # print(mycollection)
    # cursor = mycollection.find()
    # for record in cursor:
    #     print(record)
    # pass

def process_auto_mapped_rdf(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = 'rdfMappingOutput.n3'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            if "0E-10.0 ;" in line:
                line = line.replace("0E-10.0 ;", "0 ;")
                # print 'got it!'
            write_obj.write(line)
    # remove original file
    # os.remove(file_name)
    # # Rename dummy file as the original file
    # os.rename(dummy_file, file_name)