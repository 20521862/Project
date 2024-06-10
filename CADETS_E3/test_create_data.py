import os
import re
import hashlib
import sqlite3
from tqdm import tqdm

from config import *
from kairos_utils import *

filelist = ['ta1-cadets-e3-official-1.json.4']

def stringtomd5(originstr):
    originstr = originstr.encode("utf-8")
    signaturemd5 = hashlib.sha256()
    signaturemd5.update(originstr)
    return signaturemd5.hexdigest()

def check_table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None

def create_tables_if_not_exist(cur):
    # Check and create netflow_node_table if it doesn't exist
    if not check_table_exists(cur, 'netflow_node_table'):
        cur.execute('''CREATE TABLE netflow_node_table (
                        node_uuid TEXT, 
                        hash_id TEXT, 
                        src_addr TEXT, 
                        src_port TEXT, 
                        dst_addr TEXT, 
                        dst_port TEXT
                    )''')
        print("Created table netflow_node_table")

def store_netflow(file_path, cur, connect):
    # Parse data from logs
    netobjset = set()
    netobj2hash = {}
    for file in tqdm(filelist):
        with open(file_path + file, "r") as f:
            for line in f:
                if "NetFlowObject" in line:
                    try:
                        res = re.findall(
                            'NetFlowObject":{"uuid":"(.*?)"(.*?)"localAddress":"(.*?)","localPort":(.*?),"remoteAddress":"(.*?)","remotePort":(.*?),',
                            line)[0]

                        nodeid = res[0]
                        srcaddr = res[2]
                        srcport = res[3]
                        dstaddr = res[4]
                        dstport = res[5]

                        nodeproperty = srcaddr + "," + srcport + "," + dstaddr + "," + dstport
                        hashstr = stringtomd5(nodeproperty)
                        netobj2hash[nodeid] = [hashstr, nodeproperty]
                        netobj2hash[hashstr] = nodeid
                        netobjset.add(hashstr)
                    except Exception as e:
                        print(f"Error processing line: {line}\n{e}")
                        pass

    # Store data into database
    datalist = []
    for i in netobj2hash.keys():
        if len(i) != 64:
            datalist.append([i] + [netobj2hash[i][0]] + netobj2hash[i][1].split(","))

    sql = '''INSERT INTO netflow_node_table (node_uuid, hash_id, src_addr, src_port, dst_addr, dst_port)
             VALUES (?, ?, ?, ?, ?, ?)
          '''
    cur.executemany(sql, datalist)
    connect.commit()

def insert_sample_data(cur, connect):
    # Insert sample data into netflow_node_table
    sample_data = [
        ('uuid1', 'hash1', '192.168.1.1', '1234', '192.168.1.2', '5678'),
        ('uuid2', 'hash2', '192.168.2.1', '2345', '192.168.2.2', '6789'),
        ('uuid3', 'hash3', '192.168.3.1', '3456', '192.168.3.2', '7890')
    ]
    sql = '''INSERT INTO netflow_node_table (node_uuid, hash_id, src_addr, src_port, dst_addr, dst_port)
             VALUES (?, ?, ?, ?, ?, ?)
          '''
    cur.executemany(sql, sample_data)
    connect.commit()

def read_data_from_table(cur, table_name):
    sql = f"SELECT * FROM {table_name}"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    cur, connect = init_database_connection()

    # Check and create necessary tables
    create_tables_if_not_exist(cur)

    # Insert sample data
    print("Inserting sample data into netflow_node_table")
    insert_sample_data(cur, connect)

    # Read and print data from netflow_node_table
    print("Reading data from netflow_node_table")
    read_data_from_table(cur, "netflow_node_table")

