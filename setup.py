import os

homeDir = os.path.expanduser('~')

if not os.path.exists(os.path.join(homeDir, 'ScoutingServer/config')):
    os.makedirs(os.path.join(homeDir, 'ScoutingServer/config'))
if not os.path.exists(os.path.join(homeDir, 'ScoutingServer/assignments')):
    os.makedirs(os.path.join(homeDir, 'ScoutingServer/assignments'))
if not os.path.exists(os.path.join(homeDir, 'ScoutingServer/cache')):
    os.makedirs(os.path.join(homeDir, 'ScoutingServer/cache'))
    os.makedirs(os.path.join(homeDir, 'ScoutingServer/cache/teams'))
    os.makedirs(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs'))
