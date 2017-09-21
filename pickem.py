import pandas as pd

table = pd.read_html('http://www.vegasinsider.com/nfl/odds/las-vegas/money/',
                     attrs={'class': 'frodds-data-tbl'})

table[0].dropna(inplace=True, subset=[0, 2])
teams, lines = table[0][0], table[0][2]


def get_road_team(teams):
    road = teams.split('\xa0')[1]
    return road[0:road.rfind(' ')].rstrip()


def get_home_team(teams):
    return teams.split('\xa0')[2]


def get_road_lines(lines):
    second_line_start = max(lines.rfind('+'), lines.rfind('-'))
    return int(lines[0:second_line_start])


def get_home_lines(lines):
    second_line_start = max(lines.rfind('+'), lines.rfind('-'))
    return int(lines[second_line_start:])

nfl = pd.DataFrame()

nfl['road'] = teams.apply(get_road_team)
nfl['home'] = teams.apply(get_home_team)
nfl['road_odds'] = lines.apply(get_road_lines)
nfl['home_odds'] = lines.apply(get_home_lines)

nfl.set_index([nfl['road'], nfl['home']], inplace=True)

nfl['road_win'] = nfl['road_odds'] < nfl['home_odds']
nfl['winning_odds'] = nfl[['road_odds', 'home_odds']].min(axis=1)

nfl['confidence'] = 17 - nfl['winning_odds'].rank()
nfl['duplicate'] = nfl['confidence'].duplicated(keep=False)

nfl['winner'] = nfl['home']
nfl.loc[nfl['road_win'], 'winner'] = nfl['road']

print(nfl[['winner', 'winning_odds', 'confidence']])
