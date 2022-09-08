
#import packages
import os
import pandas as pd
import snowflake.connector as sc
import numpy as np
import getpass as gp

# User variables
fileName = input('Please enter name of existing file with extension:  ')
tableName = input('Please enter name of snowflake table:  ')
username = gp.getuser()

# get excel data
os.chdir('C:/users/' + username + '/desktop')
ph = np.asarray(pd.read_excel(fileName,header=None))

# Create SQL queries
qSchema = '' # select schema ex. USE SCHEMA xxxx;
qDrop = 'DROP TABLE IF EXISTS' + tableName 
qPermission = 'GRANT SELECT ON TABLE ' + tableName + ' TO ROLE PUBLIC'

qCreate = 'CREATE TABLE ' + tableName + ' (' 
i = 0

while i <  len(ph[0]):
    if i != len(ph[0])-1:
        qCreate += str(ph[0][i]).replace(' ', '_').replace('#', 'Num') + ' varchar' + ','
    else:            
        qCreate += str(ph[0][i]).replace(' ', '_').replace('#', 'Num') + ' varchar);'
    i+=1

print(ph[2303][9])
# Connect to snowflake
user = '' #snowflake user login
password = '' #snowflake password login
account = '' #snofalke account name

cnx = sc.connect(
        user=user,
        password=password,
        account=vslr)

# Execute queries
cnx.cursor().execute(qSchema)
cnx.cursor().execute(qDrop)
cnx.cursor().execute(qCreate)

qPopulate = 'INSERT INTO ' + tableName + ' values '
x = 1

while x < len(ph):
    if x % 16000 == 0: 
        cnx.cursor().execute(qPopulate)
        qPopulate = 'INSERT INTO ' + tableName + ' values '
    y = 0
    qPopulate += '('

    while y < len(ph[0]):
        if pd.isnull(ph[x][y]): 
            ph[x][y] = ''
        if x != len(ph)-1 and (x+1) % 16000 != 0 and y == len(ph[0])-1: 
            qPopulate += '\'' + str(ph[x][y]).replace('\'','') + '\'),'
        elif (x == len(ph)-1 or (x+1) % 16000 == 0) and y == len(ph[0])-1: 
            qPopulate += '\'' + str(ph[x][y]).replace('\'','') + '\');'
        else: 
            qPopulate += '\'' + str(ph[x][y]).replace('\'','') + '\','
        y+=1
    x+=1
cnx.cursor().execute(qPopulate)

cnx.cursor().execute(qPermission)

# Close snowflake connection
cnx.close()

# Print completion confirmation
print('Table creation and population completed.' + '\n')

input('You can now close this window')
    
