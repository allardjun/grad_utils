# make tweets from output of drive_ourPubs.py
# Jun allardlab.com

import pandas as pd

from grad_utils import Student


def tweet_our_pubs():
    # load list of students and their advisors

    # create dataframe
    #df_pub_list = pd.DataFexcrame(columns=['studentFirstName', 'studentLastName', 'PILastName', 'Title', 'Journal', 'Date','pmid'])

    df_pub_list = pd.read_excel('results/papers_manually_postprocessed.xlsx', index_col=0)

    for iPub, this_pub in df_pub_list.iterrows():
        tweet = 'Congratulations to UCI-MCSB student ' + this_pub['studentFirstName'].strip() + \
            ' from ' + this_pub['PILastName'] + ' lab' + \
            ' on their recent publication \"' + this_pub['Title'].rstrip('.') + '\"'+ \
            ' in ' + this_pub['Journal'] + '!'
        print(tweet)

if __name__ == "__main__":
    tweet_our_pubs()