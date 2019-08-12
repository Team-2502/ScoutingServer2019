import tbapy
import os
import json

import sensitiveInfo
from utils import *


def get_timds(team_number):
    homeDir = os.path.expanduser('~')
    TIMDs = [timd for timd in os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs')) if timd != '.DS_Store']
    return [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs/', TIMD)).read()) for TIMD in TIMDs if int(TIMD.split('-')[1]) == int(team_number)]


def get_team(team_number):
    homeDir = os.path.expanduser('~')
    teams = os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/teams'))
    return [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/teams/', team)).read()) for team in teams if int(team.split('.')[0]) == int(team_number)][0]


def calculate_defense(team_number):
    tba = tbapy.TBA(sensitiveInfo.tba_api_key())
    event = "2019dar"

    timds = get_timds(team_number)

    for timd in timds:
        alliance = timd['header']['driversStation'][:3]
        opposing_teams = [get_team(int(team[3:])) for team in tba.match(year=2019, event=event, type='qm', number=int(timd['match_number']))['alliances'][alliance]['team_keys']]
        opposing_timds = [timd_ for timd_ in [team['timds'] for team in opposing_teams] if int(timd_['match_number']) == int(timd['match_number'])]
        drops_caused = len([cycles.filter_timeline_actions([opposing_timds], actionType='drop', wasDefended=True)])
        hatch_cycle_time_decreased = stats.avg([stats.percent_difference(timd_['calculated']['undefendedHatchAverageCycleTime'], timd_['calculated']['defendedHatchAverageCycleTime']) for timd_ in opposing_timds if timd_['calculated']['defendedHatchAverageCycleTime'] != 0 and timd_['calculated']['defendedHatchAverageCycleTime'] != 0])
        cargo_cycle_time_decreased = stats.avg([stats.percent_difference(timd_['calculated']['undefendedCargoAverageCycleTime'], timd_['calculated']['defendedCargoAverageCycleTime']) for timd_ in opposing_timds if timd_['calculated']['defendedCargoAverageCycleTime'] != 0 and timd_['calculated']['defendedCargoAverageCycleTime'] != 0])
        cycle_percent_reduction = stats.avg([stats.percent_difference(timd_['calculated']['totalTeleopCycles'], get_team(int(timd_['teamNumber']))['totals']['avgTotalTeleopCycles']) for timd_ in opposing_timds if timd_['calculated']['timeDefending'] < 80])


calculate_defense(51)
