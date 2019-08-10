import openpyxl
import json
import os

homeDir = os.path.expanduser('~')
teams = [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/teams/', team)).read()) for team in os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/teams')) if team != '.DS_Store']

current_row = 3
for team in teams:
    if len(team.keys()) > 2:
        totals = ([key for key in team['totals'].keys()], 'totals')
        l3ms = ([key for key in team['l3ms'].keys()], 'l3ms')
        SDs = ([key for key in team['SDs'].keys()], 'SDs')
        maxes = ([key for key in team['maxes'].keys()], 'maxes')
        rankings = ([key for key in team['rankings'].keys()], 'rankings')
        team_abilities = ([key for key in team['team_abilities'].keys()], 'team_abilities')
        percentages = ([key for key in team['percentages'].keys()], 'percentages')
        sykes = ([key for key in team['sykesData'].keys()], 'Sykes')

        headers = [totals, l3ms, SDs, maxes, rankings, team_abilities, percentages]
        if not os.path.exists(os.path.join(os.getcwd(), 'uwu.xlsx')):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Raw Export'

            ws.cell(row=2, column=1).value = 'Number'

            current_column = 2

            for header in headers:
                ws.merge_cells(start_row=1, end_row=1, start_column=current_column,  end_column=current_column + len(header[0]) - 1)
                ws.cell(row=1, column=current_column).value = header[1]
                current_column += len(header[0])

            current_column = 2
            for header in headers:
                for key in header[0]:
                    ws.cell(row=2, column=current_column).value = key
                    current_column += 1

            wb.save(filename='uwu.xlsx')

        wb = openpyxl.load_workbook('uwu.xlsx')
        ws = wb['Raw Export']
        ws.cell(row=current_row, column=1).value = team['teamNumber']
        current_column = 2
        for header in headers:
            for key in header[0]:
                ws.cell(row=current_row, column=current_column).value = team[header[1]][key]
                current_column += 1

        current_row += 1
        wb.save('uwu.xlsx')
