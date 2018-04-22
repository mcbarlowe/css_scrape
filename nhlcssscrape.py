import sys
import datetime
import bs4
import pandas as pd
import requests
import numpy as np

def clean_height(value):
    '''
    Function to convert height meausered in feet and inches to a decimal
    value

    Input:
    value - height measured in feet and inches

    Output:
    decimal_value - height returned in feet and inches converted to a decimal
                    value of feet
    '''
    try:
        value = value.replace("'", '.').replace(' ', '').replace('"', '')
        value_list = value.split('.')
        value_list[1] = float(value_list[1])/12
        value = float(value_list[0]) + value_list[1]
        value = round(value, 2)
    except IndexError as ex:
        value = np.nan

    return value

def clean_name(value):
    '''
    Function to convert names from (last_name, first_name) to (first_name,
    last_name)

    Input:
    value - name in original setting

    Output:
    full_name - name in first_name, last_name order
    '''
    value_list = value.split(',')
    print(value_list)
    full_name = '{} {}'.format(value_list[1], value_list[0])
    print(full_name)

    return full_name


def scrape_css_headers():
    '''
    Function to scrape the headers of the rankings tables and save them to a
    list

    Inputs:
    url - url of the NHL CSS rankings website

    Outputs:
    headers - a list of the headers of the rankings table
    '''
    url = 'http://www.nhl.com/ice/draftprospectbrowse.htm?'\
          'cat=1&sort=finalRank&year=2008&pg=1'
    headers = []
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    for header in soup.find_all('th'):
        headers.append(header.text)
    headers = [x[:-1] for x in headers]
    headers.append('Year')

    return headers

def scrape_css_rankings(category, year, page):
    '''
    This function scrapes the NHL CSS scouting page and returns the
    values in a list of lists

    Inputs:
    category - a value of 1 or 2 that tells the url to scrape NA or Euro
               players

    year     - the year of scouting rankings to scrape

    page     - the page number of results to scrape

    rankings - a list on which to append the scraped values to

    Outputs:
    rankings - a list of lists that holds the rankings from the scrape
    '''

    url_base = 'http://www.nhl.com/ice/draftprospectbrowse.htm?'
    url_end = 'cat={}&sort=finalRank&year={}&pg={}'.format(category, year, page)
    page = requests.get('{}{}'.format(url_base, url_end))
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    rankings = []
    for row in soup.find_all('td'):
        rankings.append(row.text)

    rankings.pop(0)
    rankings.pop()
    rankings = list(map(str.strip, rankings))
# compiles rankings into list of lists where one list represents one player
    if str(year) in ['2008', '2010'] and str(category) == '4':
        rankings = [rankings[x:x+7] for x in range(0, len(rankings), 7)]
        for rank in rankings:
            rank.insert(0, '')
    else:
        rankings = [rankings[x:x+8] for x in range(0, len(rankings), 8)]
    for rank in rankings:
        rank.append(str(year))

    return rankings

def main():
    '''
    This script scrape all the NHL's CSS scouting reports and saves them to
    a pipe delimited file

    Inputs:
    sysarg[1] - name of the file to save the results to

    Outputs:
    rankings_file - file of pipe delimited value of all the NHL CSS central
                    scouting reports
    '''
    filename = sys.argv[1]
    rankings = []
    date = datetime.datetime.now()
    category = list(range(1, 5))
    years = list(range(2008, date.year + 1))
    headers = scrape_css_headers()
    for year in years:
        print(year)
        for player_type in category:
            print(player_type)
            new_rankings_len = 50
            page = 1
            while new_rankings_len >= 50:
                print(new_rankings_len)
                new_rankings = scrape_css_rankings(player_type, year, str(page))
                new_rankings_len = len(new_rankings)
                for rank in new_rankings:
                    rankings.append(rank)
                page += 1
    print(rankings)
    rankings_df = pd.DataFrame(rankings, columns=headers)
    print(rankings_df.head())
    rankings_df['Height'] = rankings_df['Height'].astype('str').apply(clean_height)
    rankings_df['Player'] = rankings_df['Player'].astype('str').apply(clean_name)
    print(rankings_df.head())
    rankings_df.to_csv(filename, sep='|', index=False)

if __name__ == '__main__':
    main()
