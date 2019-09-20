import os
import calculations.pullSykesData
import calculations.calculateMatch

homeDir = os.path.expanduser('~')

if not os.path.exists(os.path.join(homeDir, 'EMCC-2019Server/config')):
    os.makedirs(os.path.join(homeDir, 'EMCC-2019Server/config'))
if not os.path.exists(os.path.join(homeDir, 'EMCC-2019Server/assignments')):
    os.makedirs(os.path.join(homeDir, 'EMCC-2019Server/assignments'))
if not os.path.exists(os.path.join(homeDir, 'EMCC-2019Server/cache')):
    os.makedirs(os.path.join(homeDir, 'EMCC-2019Server/cache'))
    os.makedirs(os.path.join(homeDir, 'EMCC-2019Server/cache/teams'))
    os.makedirs(os.path.join(homeDir, 'EMCC-2019Server/cache/TIMDs'))

# calculations.pullSykesData.get_sykes_data()
