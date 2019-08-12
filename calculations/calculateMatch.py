import tbapy
import os
import json
import scipy.stats
import numpy as np
import math
import utils.stats

import sensitiveInfo


def get_team(team_number):
    homeDir = os.path.expanduser('~')
    teams = os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/teams'))
    try:
        return [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/teams/', team)).read()) for team in teams if
                int(team.split('.')[0]) == team_number][0]
    except IndexError:
        return None


def predicted_sandstorm_score(alliance):
    predicted_score = 0
    for team in alliance:
        if team['team_abilities']['startLevel2'] and team['percentages']['leftHab'] > 80:
            predicted_score += 6
        elif team['percentages']['leftHab'] > 80:
            predicted_score += 3
    return predicted_score


def predicted_teleop_score(alliance, likely_defender):
    predicted_score = 0
    for team in alliance:
        if team != likely_defender:
            predicted_score += team['p75s']['p75CargoScored'] * 3
            predicted_score += team['p75s']['p75HatchesScored'] * 2
    return predicted_score


def predicted_climb_score(alliance):
    has_lvl3 = False
    lvl2s = 0

    predicted_score = 0

    for team in alliance:
        if team['team_abilities']['climbHab3'] and not has_lvl3:
            predicted_score += 12
            has_lvl3 = True
        elif team['team_abilities']['climbHab2'] and lvl2s != 2:
            predicted_score += 6
            lvl2s += 1
        else:
            predicted_score += 3

    return predicted_score


def predicted_alliance_score(alliance, likely_defender):
    total_score = 0
    total_score += predicted_sandstorm_score(alliance)
    total_score += predicted_teleop_score(alliance, likely_defender)
    total_score += predicted_climb_score(alliance)
    return total_score


def alliance_teleop_sd(alliance):
    hatches = utils.stats.sum_sd([team['SDs']['SDHatchesScored'] * 2 for team in alliance])
    cargo = utils.stats.sum_sd([team['SDs']['SDCargoScored'] * 3 for team in alliance])

    return utils.stats.sum_sd([hatches, cargo])


def alliance_sandstorm_sd(alliance):
    # TODO
    pass


def alliance_climb_sd(alliance):
    # TODO
    pass


def sd_predicted_alliance_score(alliance):
    # sandstorm_sd = alliance_sandstorm_sd(alliance)
    teleop_sd = alliance_teleop_sd(alliance)
    # climb_sd = alliance_climb_sd(alliance)
    return teleop_sd  # utils.stats.sum_sd([sandstorm_sd, teleop_sd, climb_sd])


def get_avg_num_timds_for_alliance(alliance):
    return sum([len([team['timds'] for team in alliance])])


def find_likely_defender(teams):
    sortedDefense = [team for team in sorted(teams, key=lambda i: i['totals']['timeDefending'], reverse=True)]
    nonZeroDefense = [team for team in teams if team['totals']['timeDefending'] > 15]
    if len(nonZeroDefense) == 0:
        return None
    elif len(nonZeroDefense) == 1:
        return nonZeroDefense[0]

    else:
        if nonZeroDefense[0]['totals']['timeDefending'] > nonZeroDefense[1]['totals']['timeDefending'] + 240 or \
                nonZeroDefense[0]['totals']['avgTOC'] > nonZeroDefense[1]['totals']['avgTOC'] + 10 or \
                nonZeroDefense[1]['totals']['avgTOC'] < 15:
            return nonZeroDefense[0]
        elif sortedDefense[0]['totals']['avgTOC'] < 15:
            return nonZeroDefense[1]
        else:
            return None


def welchsTest(mean1, mean2, std1, std2, sampleSize1, sampleSize2):
    t = scipy.stats.ttest_ind_from_stats(mean1, std1, sampleSize1, mean2, std2, sampleSize2, False)[0] # False means the variances are unequal
    return t if t != np.nan else mean1 > mean2


def getDF(s1, s2, n1, n2):
    # Degrees of freedom to determine shape of Student t-distribution
    if np.nan in [s1, s2, n1, n2] or 0.0 in [n1, n2]:
        return
    try:
        numerator = ((s1 ** 4 / n1) + (s2 ** 4 / n2)) ** 2
        denominator = (s1 ** 8 / ((n1 ** 2) * (n1 - 1))) + (s2 ** 8 / ((n2 ** 2) * (n2 - 1)))
    except ZeroDivisionError:
        numerator = 0.0
        denominator = 0.0
    return numerator / denominator if denominator != 0 else 0.0


def alliance_win_chance(alliance, opp_alliance, alliance_defender, opp_alliance_defender):
    predicted_score = predicted_alliance_score(alliance, alliance_defender)
    opposing_predicted_score = predicted_alliance_score(opp_alliance, opp_alliance_defender)
    sd_predicted_score = 5 * sd_predicted_alliance_score(alliance)
    sd_opposing_predicted_score = 5 * sd_predicted_alliance_score(opp_alliance)
    sample_size = get_avg_num_timds_for_alliance(alliance)
    opposing_sample_size = get_avg_num_timds_for_alliance(opp_alliance)
    tscoreRPs = welchsTest(predicted_score, opposing_predicted_score, 0.1, 0.1, sample_size, opposing_sample_size)
    df = getDF(sd_predicted_score, opposing_predicted_score, sample_size, opposing_sample_size)
    winChance = scipy.stats.t.cdf(tscoreRPs, df)
    return winChance if not math.isnan(winChance) else 0


def get_matches():
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
        if None in match['redTeams'] or None in match['blueTeams']:
            break
        match['redTopScorer'] = [int(team['teamNumber']) for team in
                                 sorted(match['redTeams'], key=lambda i: i['totals']['avgTOC'], reverse=True)][0]
        match['blueTopScorer'] = [int(team['teamNumber']) for team in
                                  sorted(match['blueTeams'], key=lambda i: i['totals']['avgTOC'], reverse=True)][0]
        match['redLikelyDefender'] = find_likely_defender(match['redTeams'])
        match['blueLikelyDefender'] = find_likely_defender(match['blueTeams'])
        match['redPredictedPoints'] = predicted_alliance_score(match['redTeams'], match['redLikelyDefender']),
        match['bluePredictedPoints'] = predicted_alliance_score(match['blueTeams'], match['blueLikelyDefender']),
        # match['redWinPercentage'] = alliance_win_chance(match['redTeams'], match['blueTeams'], match['redLikelyDefender'], match['blueLikelyDefender']),
        # match['blueWinPercentage'] = alliance_win_chance(match['blueTeams'], match['redTeams'], match['blueLikelyDefender'], match['redLikelyDefender'])
        """
        'redPredictedRPs',
        'bluePredictedRPs',
        'predictedWinner',
        """
        print(match)


get_matches()
# TODO check if match is able to be calced fully ie if all teams have played
