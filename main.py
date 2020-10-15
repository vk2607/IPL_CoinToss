# Each team can play max 2 matches with other teams
# Each team will play atleast 3 matches

import random
from tqdm import tqdm

def intialize_data():
    # initializes a dict that stores all data
    # about the matches played and their outcomes
    teams = {0, 1, 2, 3, 4, 5, 6, 7}
    matches = dict()
    
    # maintain a set of desirable outcomes generated so far
    matches['final_outcomes'] = set()
    
    # maintain a list of teams whose 3 matches aren't completed yet
    matches['3_matches_left'] = {0, 1, 2, 3, 4, 5, 6, 7}

    for i in range(8):
        
        opponents = {0, 1, 2, 3, 4, 5, 6, 7}
        
        # remove itself from its opponents
        opponents.remove(i)

        matches[i] = {
          'opponents': opponents,
          'outcomes': ''    # stored as a string (e.g. 'WWL')
        }

        # initialize matches played with everyone to 0
        for j in opponents:
          matches[i][j] = 0

    return teams, matches

def play_match(matches, team, opponent, outcome):
    # increase count of matches played with j
    matches[team][opponent] += 1
    matches[opponent][team] += 1
    
    # append outcome
    matches[team]['outcomes'] += 'W' if outcome == team else 'L'
    matches[opponent]['outcomes'] += 'W' if outcome == opponent else 'L'
    
    # if the two teams have played against each other for 2 times, remove them from each other's opponents
    if matches[team][opponent] == 2:
        matches[team]['opponents'].remove(opponent)
        matches[opponent]['opponents'].remove(team)
    
    # add the outcomes to final_outcomes
    add_to_final_outcomes(matches, team, matches[team]['outcomes'])
    add_to_final_outcomes(matches, opponent, matches[opponent]['outcomes'])

def add_to_final_outcomes(matches, team, outcome):
    if len(outcome) == 3:
        matches['3_matches_left'].remove(team)
        matches['final_outcomes'].add(outcome)

# initialize counters
desirable_outcomes = 0
sample_space = 0

iterations = int(input('How many times do you want to run this experiment? '))

for i in tqdm(range(iterations)):

    teams, matches = intialize_data()

    # while loop schedules new matches between teams
    # run it until all teams have played at least 3 matches
    while len(matches['3_matches_left']) > 0 and len(teams) > 0:
        
        # select a random team, opponent and match outcome
        team = random.sample(teams, 1)[0]
        opponent = random.sample(matches[team]['opponents'], 1)[0]
        outcome = random.choice([team, opponent])

        play_match(matches, team, opponent, outcome)

        # remove the team from teams if they complete their 14 matches (2 against each opponent)
        if len(matches[team]['outcomes']) == 14:
            teams.remove(team)

        if len(matches[opponent]['outcomes']) == 14:
            teams.remove(opponent)

    # increment the desirable outcomes counter if condition is satisfied
    if len(matches['final_outcomes']) == 8:
        desirable_outcomes += 1
    sample_space += 1
    
probability = round(desirable_outcomes / sample_space, 4)
print(f'Probability: {probability * 100}%')

