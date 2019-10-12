import os
import json
from scipy.stats import rankdata


def calculate_rankings(team_num, current_team):
    homeDir = os.path.expanduser('~')
    teams_json = [file for file in os.listdir(os.path.join(homeDir, 'MRI-2019Server/cache/teams')) if file != '.DS_Store']
    teams = [json.loads(open(os.path.join(homeDir, 'MRI-2019Server/cache/teams/', team)).read()) for team in teams_json if int(team.split('.')[0]) != team_num] + [current_team]
    index = [int(team['teamNumber']) for team in teams].index(team_num)

    rankings = {}

    rankings['numOfTeamsUsed'] = len(teams)

    rankings['avgTOC'] = int(rankdata([team['totals']['avgTOC'] for team in teams], method='max').astype(int)[index])

    rankings['maxCargoScored'] = int(rankdata([team['maxes']['maxCargoScored'] for team in teams], method='max').astype(int)[index])
    rankings['maxHatchesScored'] = int(rankdata([team['maxes']['maxHatchesScored'] for team in teams], method='max').astype(int)[index])
    rankings['avgCargoScored'] = int(rankdata([team['totals']['avgCargoScored'] for team in teams], method='max').astype(int)[index])
    rankings['avgHatchesScored'] = int(rankdata([team['totals']['avgHatchesScored'] for team in teams], method='max').astype(int)[index])
    rankings['p75CargoScored'] = int(rankdata([team['p75s']['p75CargoScored'] for team in teams], method='max').astype(int)[index])
    rankings['p75HatchesScored'] = int(rankdata([team['p75s']['p75HatchesScored'] for team in teams], method='max').astype(int)[index])

    rankings['avgTimeClimbing'] = int(rankdata([-1 * i for i in [team['totals']['avgTimeClimbing'] for team in teams]], method='max').astype(int)[index])
    rankings['avgTimeDefending'] = int(rankdata([team['totals']['avgTimeDefending'] for team in teams], method='max').astype(int)[index])

    rankings['avgHatchCycleTime'] = int(rankdata([-1 * i for i in [team['cycle_times']['hatchOverall'] for team in teams]], method='max').astype(int)[index])
    rankings['avgCargoCycleTime'] = int(rankdata([-1 * i for i in [team['cycle_times']['cargoOverall'] for team in teams]], method='max').astype(int)[index])

    rankings['p75HatchCycleTimeUndefended'] = int(rankdata([-1 * i for i in [team['cycle_times']['p75HatchUndefended'] for team in teams]], method='max').astype(int)[index])
    rankings['p75CargoCycleTimeUndefended'] = int(rankdata([-1 * i for i in [team['cycle_times']['p75CargoUndefended'] for team in teams]], method='max').astype(int)[index])

    return rankings
