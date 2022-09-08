import imaplib
import email
import email.header
import re
import getpass
import math
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from bs4 import NavigableString
from oauth2client.service_account import ServiceAccountCredentials

M = imaplib.IMAP4_SSL('imap.gmail.com')
email_account = ''
email_password = ''
email_folder = ''

def process_mailbox(M):

    rv, data = M.search(None, "ALL")

    if rv != 'OK':
        print("No messages found!")
        return
    
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')

        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        subject = str(email.header.make_header(email.header.decode_header(msg['Subject'])))
        contents = str(email.header.make_header(email.header.decode_header(str(msg.get_payload()[1])))).replace('\n', '').replace('=', '')
        soup = BeautifulSoup(contents,'html.parser')
        tr = soup.find_all('tr')
        head = ['Request_Num', 'Submitted Date']
        line = [tr[1].contents[1].contents[1].text, tr[1].contents[1].contents[3].text]
        count = 6

        for x in range(6, len(tr)-3):
            for y in range(0, len(tr[x])):
                    if y == 0:
                        head.append(re.sub('[^a-zA-Z0-9 \n\.]', '', tr[x].contents[y].text))
                    elif y == 1: 
                        line.append(tr[x].contents[y].text) 
                    count+=1

        if num == b'1':
            array = [head] + [line]
        else:
            array.append(head)
            array.append(line)

    pop_sheet(sort_Array(array))

def sort_Array(ar):
    for x in range(0, len(ar), 2):
        if x == 0:
            longest = [x, len(ar[x])]
        else:
            if longest[1] < len(ar[x]):
                longest = [x, len(ar[x])]

    array = [ar[longest[0]]]

    for x in range(0, len(ar), 2): 
        line = []    
        skip = []
        for y in range(0, len(array[0])):           
            match = False            
            for z in range(0, len(ar[x])): 
                if z not in skip and str(ar[x][z]).lower() == str(array[0][y]).lower():
                    line.append(ar[x+1][z])
                    skip.append(z)
                    match = True
                    break
            if match == False: 
                line.append('')
        array.append(line)

    return array

def pop_sheet(arr):

    start = 'Data!B2:' # google sheet start cell ex. Data!B2:        
    
    if math.floor(len(arr[0])) / 26 <= 1:
       end = chr(math.floor(len(arr[0])/26)+65) + str(len(arr)+1)
    else:
       end = chr(math.floor(len(arr[0])/26)+64) + chr((len(arr[0])%26)+66) + str(len(arr)+1)

    range = start + end

    ssID = '' # sheet ID
    scopes = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']
	token_path = '' # file path for token

    credentials = ServiceAccountCredentials.from_json_keyfile_name(tokenPath, scopes)
    auth = build('sheets', 'v4', credentials=credentials)    

    update = { 'valueInputOption' : 'USER_ENTERED', 
                'data': 
                [
                    {
                        'majorDimension': 'ROWS', 
                        'range': range, 
                        'values': arr
                    }
                ]
            }
    test = range=re.sub(r'\d+', '', range)
    auth.spreadsheets().values().clear(spreadsheetId=ssID, range=re.sub(r'\d+', '', range), body={ }).execute()
    auth.spreadsheets().values().batchUpdate(spreadsheetId=ssID, body=update).execute()

    print('Data range updated')

try:
    rv, data = M.login(email_account, email_password)
except imaplib.IMAP4.error:
    print ("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
rv, data = M.select(email_folder)

if rv == 'OK':
    process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()