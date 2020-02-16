"""
CLU - command line utility for roborank
"""

import pandas as pd 
from collections import defaultdict

from scoring import BinaryCategoryAggregator

from statistics import mean, stdev

import argparse
import os
import logging

logger = logging.getLogger('RoboRank-CLU')
logger.setLevel(logging.WARNING)

def calc_scores_for_round(rows, us_name="us", id_col='Team Number'):
    """
    Calculate the scores for a given round.   Iterate through all commbinations of
    us + two other teams in the round.
    
    TODO:  Incorporate point value vector for binary components.
    """
    bca = BinaryCategoryAggregator()
    
    # Find "us".
    us = None
    for i in range(len(rows)):
        if rows[i]['Team Name'] == us_name:
            us = i
            break
            
    if us is None:
        raise ValueError("Our team doesn't seem to be in this round")
    
    result = list()
    
    # Iterate through the combination.
    # (Note: We only need to do half -- (us, 3, 4) is same as (us, 4, 3), e.g.)
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            if us not in (i, j):
                score = rows[i]['Balls High'] + rows[i]['Balls Low'] + \
                    rows[j]['Balls High'] + rows[j]['Balls Low']
                    
                for bc in ['Autonomous ', 'Climb ', 'Spinner Rotation', 'Spinner Colour']:
                    score += bca(rows[us][bc], rows[i][bc], rows[j][bc])
                    
                result.append((rows[us]['Round'], rows[us][id_col], rows[i][id_col], rows[j][id_col], score))
            
    return result
    
def split_into_rounds(scores):
    """
    Takes a list of dicts, or a pandas DataFrame
    each list containinig scores for a given round.
    If scores is a DataFrame, scores.to_dict(orient='records') is called to convert it to
    a list of dicts.
    """
    
    if isinstance(scores, pd.DataFrame):
        scores = scores.to_dict(orient='record')
        
    result = defaultdict(list)
        
    for row in scores:
        result[row['Round']].append(row)
        
    return result

def aggregate_scores(scores, sorting=True):
    """
    Takes a list of tuples, each touple has round#, indexes for us and two other teams, and 
    score for that combination of teams.
    
    Uses the other teams to index a dict of lists of scores.
    
    For each list of scores we calculate a mean and stddev, and a final
    score that is the quotient of these two iff the stddev > 0.  This gives the 
    weighted score.0
    """
    
    accum = defaultdict(list)
    
    for tup in scores:
        accum[(tup[2], tup[3])].append(tup[4])
    
    result = list()
    for team, scores in accum.items():
        m = mean(scores)
        s = stdev(scores)
        result.append((team, m, s, m / s if s > 0 else m))
        
    if sorting:
        result = sorted(result, key=lambda x: x[3], reverse=True)
    
    return result
    
    
def read_raw_scores(score_file):
    """
    Reads in an excell file with the scores and returns a list of dictionaries, 
    one dict per round.  Each of these is a round number and a list of dicts
    encoding the scores for that round.
    """
    return pd.read_excel(score_file).fillna(0).to_dict(orient='records')
    
    
def main():
    
    global logger
    
    # Argv parsing ...
    parser = argparse.ArgumentParser(description='roborank cmd line util: process scores in excel spreadsheet')
    parser.add_argument('score_files', metavar='SCORES', type=str, nargs='+')
    parser.add_argument('-o', '--output', type=str, dest='outfile', help='Output to FILE')
    #parser.add_argument('--debug', action='store_true')  # just for testing purposes
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose', help="Give play-by-play of what's happening")
    
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
        
    raw_scores = list()
    
    for score_file in args.score_files:
        logger.info('Reading score file "%s"', score_file)
        score_dict = read_raw_scores(score_file)
        
        logger.info('Splitting into rounds')
        rounds = split_into_rounds(score_dict)
        
        logger.info('Calculating scores')
        for r in rounds.values():
            raw_scores.extend(calc_scores_for_round(r))
    
    logger.info('Aggregating %d scores from %d rounds', len(raw_scores), len(rounds))
    result = pd.DataFrame(aggregate_scores(raw_scores), columns = ['Team Pair', 'Mean Score', 'Std Dev', 'Adj Score'])
    
    file_parts = os.path.splitext(args.score_files[0])
    
    logger.info('Writing results to %s-output%s', *file_parts)
    result.to_excel("{0}-output{1}".format(*file_parts))
    
    return 0
    
if __name__ == '__main__':
    main()