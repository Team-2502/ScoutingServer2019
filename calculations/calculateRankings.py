import os
import json


def calculate_rankings(team_num, current_team):
    homeDir = os.path.expanduser('~')
    teams_json = os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/teams'))
    teams = [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/teams/', team)).read()) for team in teams_json] + [current_team]

    rankings = {}

    rankings['numOfTeamsUsed'] = len(teams)

    print([int(team['teamNumber']) for team in sorted(teams, key=lambda i: i['totals']['avgTOC'])])
    rankings['avgTOC'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['totals']['avgTOC'])].index(team_num) + 1

    rankings['maxCargoScored'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['maxes']['maxCargoScored'], reverse=True)].index(team_num) + 1
    rankings['maxHatchesScored'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['maxes']['maxHatchesScored'], reverse=True)].index(team_num) + 1
    rankings['avgCargoScored'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['totals']['avgCargoScored'], reverse=True)].index(team_num) + 1
    rankings['avgHatchesScored'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['totals']['avgCargoScored'], reverse=True)].index(team_num) + 1
    rankings['p75CargoScored'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['p75s']['p75CargoScored'], reverse=True)].index(team_num) + 1
    rankings['p75HatchesScored'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['p75s']['p75HatchesScored'], reverse=True)].index(team_num) + 1

    rankings['avgTimeClimbing'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['totals']['avgTimeClimbing'])].index(team_num) + 1
    rankings['avgTimeDefending'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['totals']['avgTimeDefending'])].index(team_num) + 1

    rankings['avgHatchCycleTime'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['cycle_times']['hatchOverall'])].index(team_num) + 1
    rankings['avgCargoCycleTime'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['cycle_times']['cargoOverall'])].index(team_num) + 1

    rankings['p75HatchCycleTimeUndefended'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['cycle_times']['p75HatchUndefended'])].index(team_num) + 1
    rankings['p75CargoCycleTimeUndefended'] = [team['teamNumber'] for team in sorted(teams, key=lambda i: i['cycle_times']['p75CargoUndefended'])].index(team_num) + 1

    return rankings


if __name__ == '__main__':
    calculate_rankings(2337)
