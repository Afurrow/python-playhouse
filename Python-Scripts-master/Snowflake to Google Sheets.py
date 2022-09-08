# import packages
import snowflake.connector as sc
import numpy as np
from googleapiclient import discovery
from oauth2client import file, client, tools

ssId = '' # Google Sheet ID
wsRespRange = '' # Sheet Range excluding final row number ex: Responses!E2:E 
snow_user='' # snowflake user name
snow_password='' # snowflake password
snow_account='' # snowflake account
query = ''' 

''' # sql query

# Get data from google sheets
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    return creds

creds = get_credentials()

service = discovery.build('sheets', 'v4', credentials=creds)

request = service.spreadsheets().values().batchGet(spreadsheetId=ssId, ranges=wsRespRange)
response = request.execute()

# Connect to snowflake run query
cnx = sc.connect(
        user=snow_user,
        password=snow_password,
        account=snow_account)

snowResponse = cnx.cursor().execute(query)
snowResults = snowResponse.fetchall()
cnx.close()
result = np.asarray([[x[0] for x in snowResponse.description]] + snowResults).tolist()

# clear range 
try: 
    service.spreadsheets().values().clear(spreadsheetId=ssId, range=wsRespRange).execute()
    print(f'{wsRespRange} has been cleared')
except:
    print(f'Unable to clear range: {sys.exc_info()[0]}')

# populate query data to google sheet
wsDataRange = wsRespRange + str(len(result))
data = { 'range': wsDataRange, 'values': result }
body = { 'valueInputOption': 'USER_ENTERED', 'data': data }

try:
    service.spreadsheets().values().batchUpdate(spreadsheetId=ssId, body=body).execute()
    print(f'{wsDataRange} has been updated with Query Results')
except:
    print(f'Unable to update range: {sys.exc_info()[0]}')