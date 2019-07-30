import os
import json


def calculate_team(team_number):
    team = {'teamNumber': team_number}

    timds = get_TIMDS(team_number)
    lfm_timds = sorted(timds, key=lambda timd: timd.get('matchNumber'))[-4:]
    team['timds']: get_TIMDS(team_number)

    team_abilities = {}
    # Can ground pickup cargo
    # Can ground pickup hatch
    # Can climb 2/3
    # Can place Level 2/3

    defense = {}

    totals = {}
    # hatches/cargo placed
    # fouls
    # cycles to level 1/2/3
    # cycles to rocket/cs

    averages = {}
    # avg cycles hatch/cargo
    # avg cycle time hatch/cargo
    # avg cycles rocket/cs
    # avg cycle times hatch/cargo to rocket/cs

    lfms = {}
    # lfm cycles hatch/cargo
    # lfm cycle time hatch/cargo
    # lfm cycles rocket/cs
    # lfm cycle times hatch/cargo to rocket/cs

    p75s = {}
    # p75 cycles hatch/cargo
    # p75 cycle time hatch/cargo
    # p75 cycles rocket/cs
    # p75 cycle times hatch/cargo to rocket/cs
    # undefended and defended

    stds = {}
    # std cycles hatch/cargo
    # std cycle time hatch/cargo
    # std cycles rocket/cs
    # std cycle times hatch/cargo to rocket/cs
    # undefended and defended

    percentages = {}
    # percent defense
    # percent incap
    # percent no show
    # percent hatches/cargo
    # percent rocket
    # percent cs
    # percent level 1/2/3
    # percent left hab
    # percent climbed
    # percent climb succeeded
    # percent place hatch succeed
    # percent place cargo succeed
    # percent place cargo/hatch 1/2/3 succeed


def get_TIMDS(team_number):
    homeDir = os.path.expanduser('~')
    TIMDs = os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs'))
    return [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs/', TIMD)).read()) for TIMD in TIMDs if TIMD.split('-')[1] == team_number]
