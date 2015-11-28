#!/usr/bin/env python

"""
Backs up and restores a settings file to Dropbox.
This is an example app for API v2. 
"""

import sys
import os 
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

from connectors import CloudConnector

# Add OAuth2 access token here. 
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
#TOKEN = 'vlOs9aR1WXAAAAAAAAAABdEBrYMtqS4KPGKONq6UVoALWXGN0ulU3le6CUqrf3ZT'

LOCALFILE = 'my-file.txt'
BACKUPPATH = '/my-file-backup.txt'

class DropboxConnector(CloudConnector):

  def __init__(self, config):
    if (len(config.get('token')) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")
    print("Creating a Dropbox object...")
    self.dbx = dropbox.Dropbox(config.get('token'))

  def validate(self):
    # Check that the access token is valid
    try:
        self.dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

  def upload(self, filename):
    with open(filename, 'r') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        target_path = os.path.basename(filename)
        print("Uploading " + filename + " to Dropbox as /" + target_path + "...")
        try:
            self.dbx.files_upload(f, "/" + target_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

  def download(self, filename, to_file):
    self.dbx.files_download_to_file(to_file, filename, None)

 
# Uploads contents of LOCALFILE to Dropbox
def backup(filename):
    with open(filename, 'r') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        target_path = os.path.basename(filename)
        print("Uploading " + filename + " to Dropbox as /" + target_path + "...")
        try:
            dbx.files_upload(f, "/" + target_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

def select_revision(filename):
    # Get the revisions for a file (and sort by the datetime object, "server_modified")
    print("Finding available revisions on Dropbox...")
    revisions = sorted(dbx.files_list_revisions(filename, limit=3).entries,
                       key=lambda entry: entry.server_modified)

    for revision in revisions:
        print(revision.rev, revision.server_modified)

    # Return the oldest revision (first entry, because revisions was sorted oldest:newest)
    return revisions[0].rev

def get_file(filename, to_file): 
  dbx.files_download_to_file(to_file, filename, None)

if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    # Create a backup of the current settings file
    backup(LOCALFILE)

    get_file("/" + LOCALFILE, "output.txt")

    print("Done!")
