#!/usr/bin/python
# Include the Dropbox SDK
import os
import sys
import time
import json
import dropbox
import pyperclip

# Check if system executable exists, and return full path
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return False

# Open notification
def notification(message):
    if notify != False:
        os.system(notify + ' -i gtk-dialog-infor -t 30000 -- "Screenshot Uploader" "' + message + '"')
    else:
        print message

# check if required executables exist
scrot = which('scrot')
notify = which('notify-send')
if scrot == False:
    notification('Required system executable (scrot) is not available. Install it and try again.')
    sys.exit()

# Get your app key and secret from the Dropbox developer website
app_key = ''
app_secret = ''

#flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# Have the user sign in and authorize this token
#authorize_url = flow.start()
#print '1. Go to: ' + authorize_url
#print '2. Click "Allow" (you might have to log in first)'
#print '3. Copy the authorization code.'
#code = raw_input("Enter the authorization code here: ").strip()

# This will fail if the user enters an invalid authorization code
#access_token, user_id = flow.finish(code)
#print access_token
access_token = ''

client = dropbox.client.DropboxClient(access_token)

# Set screenshot filename
date = time.strftime("%d-%m-%Y-%H.%M.%S", time.localtime())
file = '/Screenshots/SS-' + date + '.png'

# Make the screenshot
command = 'scrot -s ~/Dropbox' + file
os.system(command)

# wait for the file to upload
missing = True
counter = 0
while missing == True and counter < 10:
    try:
        client.get_file(file)
        missing = False
    except:
        counter += 1
        time.sleep(1)

# Check if file was uploaded
if missing == True:
    notification('Unable to obtain share link. File upload did not complete in time.')
    sys.exit()

# Get the share link
link = client.share(file)
pyperclip.copy(link['url'])

# dumb workaround to paste issue
os.system('echo ' + link['url'] + ' | xclip')

notification('Your screenshot was uploaded and link copied to clipboard (' + link['url'] + ')')
