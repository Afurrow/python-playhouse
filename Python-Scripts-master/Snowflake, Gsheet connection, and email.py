#! Python3

import os, sys
import snowflake.connector as sc
import numpy as np
import pandas as pd
import smtplib, ssl
import list_to_html
import codecs
from datetime import date
from googleapiclient import discovery
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up variables
snow_user = "" # snowflake user name
snow_password = "" # snowflake password
snow_account = "" # snow flake account name
gsheet_id = "" # Google sheet ID
gsheet_range = "" # google sheet range including sheet name ex: sheet1!A2:B
gmail_from = "" # email to send from
gmail_login = "" # gmail login
gmail_password = "" # base64 password
query = '''

''' # enter snowflake query

# Get warehouse data from google sheets
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

warehouses = service.spreadsheets().values().get(
  spreadsheetId = gsheet_id, range = gsheet_range
).execute()

warehouse_dict = { k: v for k, v in warehouses['values'] }

# Get sql Data
cnx = sc.connect(
        user=snow_user,
        password=snow_password,
        account=snow_account) 

snow_response = cnx.cursor().execute(query)
snow_results = snow_response.fetchall()
cnx.close()
sql_head = [x[0] for x in snow_response.description]
sql_result = np.asarray(snow_results).tolist()

unique_reports = set([x[0] for x in sql_result])
unique_sources = set([x[12] for x in sql_result])
data_dict = {}

for source in unique_sources:
  data_dict[source] = {}
  for report in unique_reports:
    data_dict[source][report] = [x[1:-1] for x in sql_result if x[12] == source and x[0] == report]
    data_dict[source][report].insert(0, sql_head[1:-1])

# compose email
for key, value in data_dict.items():
  send_email = False
  cur_date = date.today()
  try:
    gmail_to = warehouse_dict[key]
  except:
    gmail_to = "" # send to different email in case of error

  subject = f"{key} Transfer report {cur_date}"
  html = '''

  ''' # enter html starter text

  for key2, value2 in value.items():
    if len(value2) > 1:
      html += f"<h2>{key2}</h2>"
      html += list_to_html.list_to_html(value2)
      html += "<br><br>"
      send_email = True

  if send_email:
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = gmail_from
    message['To'] = gmail_to 
    message.attach(MIMEText(html, 'html'))

    try:
      with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context()) as server:
        server.login(gmail_login, str(codecs.decode(gmail_password.encode(), 'base64'))[2:-1])
        server.sendmail(
              gmail_from, gmail_to, message.as_string()
        ) 
        print(f"Transfer email sent for {key}") # print success message
        # pass
        # break
    except:
      print(f"Failed to send email for {key}: {sys.exc_info()[0]}") # print error message

# Format data for corporate Email
corporate_dict = {}
corporate_dict["Not Yet Shipped"] = [x[1:-1] for x in sql_result if x[0] == "Not Yet Shipped"]
corporate_dict["Not Yet Shipped"].insert(0, sql_head[1:-1])
corporate_dict["Not Yet Received"] = [x[1:-1] for x in sql_result if x[0] == "Not Yet Received"]
corporate_dict["Not Yet Received"].insert(0, sql_head[1:-1])

# Compose Corporate Email
html = "<p>The following transfers were emailed to their respective offices.</p><br>"
for key, value in corporate_dict.items():
  html += f"<h2>{key}</h2>"
  html += list_to_html.list_to_html(value)
  html += "<br><br>"

# Send Corporate Email
subject = f"Transfer report {cur_date}"
gmail_to = "" # who to send to separated by commas

message = MIMEMultipart('alternative')
message['Subject'] = subject
message['From'] = gmail_from
message['To'] = gmail_to
message.attach(MIMEText(html, 'html'))

try:
  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context()) as server:
    server.login(gmail_login, str(codecs.decode(gmail_password.encode(), 'base64'))[2:-1])
    server.sendmail(
          gmail_from, gmail_to, message.as_string()
    ) 
    print(f"Corporate email sent") # success confirmation message
except: 
  print(f"Failed to send Corporate Email: {sys.exc_info()[0]}") # error confirmation message
