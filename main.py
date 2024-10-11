# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.

import requests as r
#import getpass
import os

# prompt to enter username and password
user = 'cstevens5'      # Input NASA Earthdata Login Username
password = '5CvyDUA/ew@6!b?'

# post username and password
api = 'https://appeears.earthdatacloud.nasa.gov/api/'  # Set the AρρEEARS API to a variable
token_response = r.post('{}login'.format(api), auth=(user, password)).json() # Insert API URL, call login service, provide credentials & return json
del user, password                                                           # Remove user and password information
print(token_response)                                                        # Print response

## SET INPUT DIRECTORY ##
inDir = 'F:/PFET/HLS/hlss/'           # IMPORTANT: Update to reflect directory on your OS

# create dir if it does not exist
if not os.path.exists(inDir):
    print(f'Creating output directory: {format(inDir)}')
    os.makedirs(inDir)     # Create the parent directory if it doesn't exist
os.chdir(inDir)

token = token_response['token']                      # Save login token to a variable
head = {'Authorization': 'Bearer {}'.format(token)}  # Create a header to store token information, needed to submit a request

#geoloc_001_dict = {
    #'2021': 'd2c014e2-b2b5-468f-8552-daf9db2b80df'
    #'2022': 'ab613c72-65be-49aa-8ede-d2c39f12c4ec',
    #'2023': 'eb8f345b-bfee-441f-9d78-4efaf26a921a'
#}

#hlsl_dict = {
    # '2021_1': '2578ba09-324c-43cd-a8c9-c49fa51e870c',
    # '2021_2': 'ca604806-a11d-4003-aff0-bbdcc59cf031'
#     '2022_1': 'ee69bfbe-3fe8-4c4a-8395-afa6290e333f',
#     '2022_2': 'f2885235-7b7e-498b-b48f-f022c82f5259',
#     '2023_1': 'f6d873de-ce67-4035-a297-92055687b730',
#     '2023_2': '8f0f2ca5-38f8-40a0-aaaa-328fef1f4d8c'
#}

hlss_dict = {
    '2021_1': '40a26c2b-ca5c-4bfe-9d18-931745c8a5dc',
    '2021_2': '03607fb0-915c-436e-bb6b-843efdfd2080'
}

## SET LOOP DICT
loop_dict = hlss_dict

# emis002_dict = {
#     '2022_2': '0a7fed8b-4674-4d44-a9a3-84e7705f6f2c',
#     '2023_1': 'cadaa2f0-ca4a-45f5-bd58-c6ff4c2f9cb5',
#     '2023_2': 'cce11bd0-f580-4f9d-952d-f8307b0b12e5'
# }

# emis001_dict = {
#     '2021_1': '6493a337-92fd-4220-a6b4-9ee1b430ff4f',
#     '2021_2': 'e2c6c4e7-6325-409f-9a2b-cfbad239ff2f',
#     '2022_1': '7b67e07d-2e8b-4595-825a-43ab05398f5a',
#     '2022_2': '2b47048b-99bc-43a1-b9a9-7f207f94e53b'
# }

#cloud_dict = {
    #'2021': '283255e4-fbc7-4336-b248-e0ee37222a1e',
    #'2022': 'a77bd44f-aa8c-4f05-8f5b-9cc04a447ac6',
    #'2023': 'e116ea1c-23af-43f4-8472-afc77f7f5078'
#}

# geoloc_dict = {
#     '2022': 'aa0b2e25-02a3-4cd4-9f43-f85e2fa37bdb',
#     '2023': 'fcbe36f7-f9a3-469c-b4ec-91a099540168'
# }

## ECOSTRESS emissivity
# [X] 2022_1 - '6f84f7d9-ae6f-488a-90c5-49a21b03f4ae'
# [X] 2022_2 - '1d8a6669-8454-428c-aa92-9d165f3b60c1'
# [X] 2023_1 - 'f928775d-f3dc-4229-ac24-f14ddccb2107'
# [X] 2023_2 - '5f0ef968-92c5-4c0d-9140-c9d4d12e05ed'

## geolocation 002
# [X] 2022 - 'aa0b2e25-02a3-4cd4-9f43-f85e2fa37bdb'
# [X] 2023 - 'fcbe36f7-f9a3-469c-b4ec-91a099540168'

## geolocation 001
# [X] 2022 - 'ab613c72-65be-49aa-8ede-d2c39f12c4ec'
# [X] 2023 - 'eb8f345b-bfee-441f-9d78-4efaf26a921a'

## HLSS
# [X] hlss_2022_1 - af2c30e4-f1ce-4ae4-bd3d-8760fac886a8
# [X] hlss_2022_2 - d80c2905-c4c9-4ac4-90a0-12a3c4f3a7a1
# [X] hlss_2023_1 - 96bea4bc-fe07-491d-a387-b34def0acb49
# [X] hlss_2023_2 - 2aa33b67-3413-4bc1-87f7-dbcd173633b4

for key in loop_dict:
    print(f'working on {key}...')

    task_name = key # manually set task name
    task_id = loop_dict.get(key) # in AppEEARS 'download list' this is the code following '/bundle/'

    destDir = os.path.join(inDir, task_name)                # Set up output directory using input directory and task name
    if not os.path.exists(destDir):
        print(f'Creating output directory: {format(destDir)}')
        os.makedirs(destDir)     # Create the output directory

    #
    bundle = r.get('{}bundle/{}'.format(api,task_id), headers=head).json()  # Call API and return bundle contents for the task_id as json
    #bundle                                                    # Print bundle contents

    files = {}                                                       # Create empty dictionary
    for f in bundle['files']: files[f['file_id']] = f['file_name']   # Fill dictionary with file_id as keys and file_name as values
    #files

    # download files
    for f in files:
        dl = r.get('{}bundle/{}/{}'.format(api, task_id, f), headers=head, stream=True, allow_redirects = 'True')  # Get a stream to the bundle file
        if files[f].endswith('.tif'):
            filename = files[f].split('/')[1]
        else:
            filename = files[f]
        filepath = os.path.join(destDir, filename)                                                       # Create output file path
        with open(filepath, 'wb') as f:                                                                  # Write file to dest dir
            for data in dl.iter_content(chunk_size=8192): f.write(data)

    print(f'\nFinished with {task_name}, downloaded files can be found at: {format(destDir)}\n\n')