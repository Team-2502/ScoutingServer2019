import tbapy
import os
import json

import sensitiveInfo


def get_team(team_number):
    homeDir = os.path.expanduser('~')
    teams = os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/teams'))
    return [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/teams/', team)).read()) for team in teams if int(team.split('.')[0]) == team_number][0]


def find_likely_defender(teams):
    sortedDefense = [team for team in sorted(teams, key=lambda i: i['totals']['timeDefending'], reverse=True)]
    nonZeroDefense = [team for team in teams if team['totals']['timeDefending'] > 15]
    print([team['teamNumber'] for team in nonZeroDefense])
    if len(nonZeroDefense) == 0:
        return None
    elif len(nonZeroDefense) == 1:
        return nonZeroDefense[0]
    else:
        if nonZeroDefense[0]['totals']['timeDefending'] > nonZeroDefense[1]['totals']['timeDefending'] + 240 or nonZeroDefense[0]['totals']['avgTOC'] > nonZeroDefense[1]['totals']['avgTOC'] + 10 or nonZeroDefense[1]['totals']['avgTOC'] < 15:
            return nonZeroDefense[0]
        elif sortedDefense[0]['totals']['avgTOC'] < 15:
            return nonZeroDefense[1]
        else:
            return None


tba = tbapy.TBA(sensitiveInfo.tba_api_key())
event = "2019dar"

# Get a list of all qualifying matches at an event
try:
    matches = [match for match in tba.event_matches(event, simple=True) if match['comp_level'] == 'qm']

# TODO Make this except clause more specfic
except:
    print("Error getting matches from TBA, check event and API keys.")
    exit(1)


for tba_match in matches:
    match = {
        'matchNumber': tba_match['match_number'],
        'redAllianceNumbers': [int(team[3:]) for team in tba_match['alliances']['red']['team_keys']],
        'blueAllianceNumbers': [int(team[3:]) for team in tba_match['alliances']['blue']['team_keys']]
    }
    match['redTeams'] = [get_team(team_number) for team_number in match['redAllianceNumbers']]
    match['blueTeams'] = [get_team(team_number) for team_number in match['blueAllianceNumbers']]
    match['redTopScorer'] = [int(team['teamNumber']) for team in sorted(match['redTeams'], key=lambda i: i['totals']['avgTOC'], reverse=True)][0]
    match['blueTopScorer'] = [int(team['teamNumber']) for team in sorted(match['blueTeams'], key=lambda i: i['totals']['avgTOC'], reverse=True)][0]
    match['redLikelyDefender'] = find_likely_defender(match['redTeams'])
    match['blueLikelyDefender'] = find_likely_defender(match['blueTeams'])
    """"
    'redPredictedPoints',
    'bluePredictedPoints',
    'redPredictedRPs',
    'bluePredictedRPs',
    'predictedWinner',
    'redWinPercentage',
    'blueWinPercentage'
    """
    print(match)
