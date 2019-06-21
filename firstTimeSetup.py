import json
import os

homeDir = os.path.expanduser('~')


slackAPIKey = "0"
# TODO Set up Slack to receive updates

# Bluetooth MAC Addresses of the Tablets
MACAddresses = {
    'scout1': '44:65:0D:19:CE:61',
    'scout2': '84:D6:D0:C9:57:50',
    'scout3': '50:F5:DA:D7:35:7C',
    'scout4': 'AC:63:BE:AA:CA:46',
    'scout5': 'AC:63:BE:D7:92:FC',
    'scout6': '50:F5:DA:82:55:0E',
    'scout7': 'AC:63:BE:D9:BC:88'
}
# TODO Confirm that they are zeroes and not the letter O
# TODO Remember to update if tablets are factory reset

if not os.path.exists(os.path.join(homeDir, 'ScoutingData/config')):
    os.makedirs(os.path.join(homeDir, 'ScoutingData/config'))
if not os.path.exists(os.path.join(homeDir, 'ScoutingData/assignments')):
    os.makedirs(os.path.join(homeDir, 'ScoutingData/assignments'))

with open(os.path.join(homeDir, 'ScoutingData/config/ScoutMACAddresses.json'), 'w') as f:
    json.dump(MACAddresses, f)

with open(os.path.join(homeDir, 'ScoutingData/config/SlackAPIKey.txt'), 'w') as f:
    f.write(slackAPIKey)
