# Include the Dropbox SDK
import os
import sys
import time
import json
import dropbox
import pyperclip

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

# make the screen cap
f = os.popen("date +%Y-%m-%d-%H-%M-%S")
date = f.read().rstrip()
file = '/Screenshots/SS-' + date + '.png'
command = 'scrot -s /home/slax0r/Dropbox' + file

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


# Get the share link
link = client.share(file)
pyperclip.copy(link['url'])

# dumb workaround to paste issue
os.system('echo ' + link['url'] + ' | xclip')

os.system('/usr/bin/notify-send -i gtk-dialog-infor -t 30000 -- "Screenshot uploaded" "Your screenshot was uploaded and link copied to clipboard (' + link['url'] + ')"')
