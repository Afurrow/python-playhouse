import pysftp
import sys
import os

host = "" # sftp host 
password = "" # sftp password
username = "" # sftp username
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None 

with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
    print('Connection established')
    directory_structure = sftp.listdir()
	dest_folder_path = '' # folder path
    for folder in directory_structure:
      os.mkdir(dest_folder_path + folder)
      sftp.chdir(None)
      sftp.chdir(folder)
      folderdir = sftp.listdir()
      for file in folderdir:
        remotepath = file;
        localpath = dest_folder_path + folder + '/' + file
        sftp.get(remotepath, localpath)