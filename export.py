import openpyxl
import json
import os

homeDir = os.path.expanduser('~')
teams = [json.loads(open(os.path.join(homeDir, 'EMCC-2019Server/cache/teams/', team)).read()) for team in os.listdir(os.path.join(homeDir, 'EMCC-2019Server/cache/teams')) if team != '.DS_Store']

totals = ([key for key in teams[0]['totals'].keys()], 'totals')
l3ms = ([key for key in teams[0]['l3ms'].keys()], 'l3ms')
SDs = ([key for key in teams[0]['SDs'].keys()], 'SDs')
maxes = ([key for key in teams[0]['maxes'].keys()], 'maxes')
rankings = ([key for key in teams[0]['rankings'].keys()], 'rankings')
team_abilities = ([key for key in teams[0]['team_abilities'].keys()], 'team_abilities')
percentages = ([key for key in teams[0]['percentages'].keys()], 'percentages')
# sykes = ([key for key in teams[0]['sykes'].keys()], 'sykes')
cycles = ([key for key in teams[0]['cycle_times'].keys()], 'cycle_times')

headers = [totals, l3ms, SDs, maxes, rankings, team_abilities, percentages, cycles]  # [sykes]


wb = openpyxl.load_workbook('paly_from_8th.xlsx')
ws = wb['Raw Export']
ws.cell(row=1, column=1).value = 'Number'

current_column = 2

for header in headers:
    for key in header[0]:
        ws.cell(row=1, column=current_column).value = key
        current_column += 1

current_row = 2
for team in teams:
        current_column = 2
        ws.cell(row=current_row, column=1).value = team['teamNumber']

        for header in headers:
            for key in header[0]:
                ws.cell(row=current_row, column=current_column).value = team[header[1]][key]
                current_column += 1

        template = wb['Team Template']
        team_sheet = wb.copy_worksheet(template)
        team_sheet.title = str(team['teamNumber'])

        team_sheet['A1'] = team['teamNumber']
        team_sheet['A2'] = "-"         # team['sykes']['teamName']

        team_sheet['B4'] = "-"         # team['pitscouting']['length']
        team_sheet['B5'] = "-"         # team['pitscouting']['width']
        team_sheet['B6'] = team['team_abilities']['placeLevel2']
        team_sheet['B7'] = team['team_abilities']['placeLevel3']
        team_sheet['B8'] = team['team_abilities']['startLevel2']
        team_sheet['B9'] = team['team_abilities']['climbHab2']
        team_sheet['B10'] = team['team_abilities']['climbHab3']
        team_sheet['B11'] = team['team_abilities']['placeCargo']
        team_sheet['B12'] = team['team_abilities']['placeHatch']
        team_sheet['A13'] = team['pitscouting']['drivetrain']   # This is in A because it is merged with column B

        team_sheet['B15'] = team['percentages']['percentOfTotalTeleopDefending']
        team_sheet['B16'] = team['totals']['avgTimeClimbing']

        team_sheet['E5'] = team['cycle_times']['hatchL1']
        team_sheet['E6'] = team['cycle_times']['cargoL1']
        team_sheet['E7'] = team['cycle_times']['hatchUndefended']
        team_sheet['E8'] = team['cycle_times']['hatchDefended']
        team_sheet['E9'] = team['cycle_times']['cargoUndefended']
        team_sheet['E10'] = team['cycle_times']['cargoDefended']
        team_sheet['E13'] = team['cycle_times']['p75HatchL1']
        team_sheet['E14'] = team['cycle_times']['p75CargoL1']
        team_sheet['E15'] = team['cycle_times']['p75HatchUndefended']
        team_sheet['E16'] = team['cycle_times']['p75HatchDefended']
        team_sheet['E17'] = team['cycle_times']['p75CargoUndefended']
        team_sheet['E18'] = team['cycle_times']['p75CargoDefended']

        team_sheet['H5'] = team['totals']['avgHatchTeleop']
        team_sheet['H6'] = team['totals']['avgCargoTeleop']
        team_sheet['H7'] = team['totals']['avgPiecesScoredRocket']
        team_sheet['H8'] = team['totals']['avgPiecesScoredCargoShip']
        team_sheet['H9'] = team['totals']['avgCargoScoredL1'] + team['totals']['avgHatchesScoredL1']
        team_sheet['H10'] = team['totals']['avgCargoScoredL3'] + team['totals']['avgHatchesScoredL3']

        team_sheet['H13'] = team['p75s']['p75HatchTeleop']
        team_sheet['H14'] = team['p75s']['p75CargoTeleop']
        team_sheet['H15'] = team['p75s']['p75PiecesScoredRocket']
        team_sheet['H16'] = team['p75s']['p75PiecesScoredCargoShip']
        team_sheet['H17'] = team['p75s']['p75CargoScoredL1'] + team['p75s']['p75HatchesScoredL1']
        team_sheet['H18'] = team['p75s']['p75CargoScoredL3'] + team['p75s']['p75HatchesScoredL3']

        team_sheet['K4'] = team['percentages']['percentMatchesClimbHab1']
        team_sheet['K5'] = team['percentages']['percentMatchesClimbHab2']
        team_sheet['K6'] = team['percentages']['percentMatchesClimbHab3']
        team_sheet['K7'] = team['percentages']['hab3ClimbSuccessRate']
        team_sheet['K8'] = team['percentages']['hab2ClimbSuccessRate']

        team_sheet['K14'] = team['percentages']['percentMatchesStartHab1']
        team_sheet['K15'] = team['percentages']['percentMatchesStartHab2']
        team_sheet['K16'] = team['percentages']['leftHab']
        team_sheet['K17'] = team['totals']['avgHatchesScoredSandstorm']
        team_sheet['K18'] = team['totals']['avgCargoScoredSandstorm']

        team_sheet['N5'] = team['l3ms']['l3mHatchesScored']
        team_sheet['N6'] = team['l3ms']['l3mCargoScored']
        team_sheet['N7'] = team['l3ms']['l3mPiecesScoredRocket']
        team_sheet['N8'] = team['l3ms']['l3mPiecesScoredCargoShip']
        team_sheet['N9'] = team['l3ms']['l3mCargoScoredL1'] + team['l3ms']['l3mHatchesScoredL1']
        team_sheet['N10'] = team['l3ms']['l3mCargoScoredL3'] + team['l3ms']['l3mHatchesScoredL3']

        team_sheet['N13'] = team['cycle_times']['l3mHatchL1']
        team_sheet['N15'] = team['cycle_times']['l3mCargoL1']
        team_sheet['N15'] = team['cycle_times']['l3mHatchUndefended']
        team_sheet['N15'] = team['cycle_times']['l3mHatchDefended']
        team_sheet['N15'] = team['cycle_times']['l3mCargoDefended']
        team_sheet['N15'] = team['cycle_times']['l3mCargoUndefended']

        current_row += 1
        wb.save('paly_from_8th.xlsx')
