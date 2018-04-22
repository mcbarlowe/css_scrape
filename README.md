# NHL Central Scouting Report Scraper

This is a script that will scrape all the data available from the
[NHL's Central Scouting rankings](http://www.nhl.com/ice/draftprospectbrowse.htm?cat=2&sort=finalRank&year=2018)
and compile them into one large pipe delimited file. Any missing
data in the tables will be replaced with an empty string `''` like
this so you can filter it that way as a lot of the earlier year
rankings are missing data.

# Running the Script

The easiest way to run the script is to create a virtual envrionment
and clone the repo into the directory you want using these steps.
These are native for a Mac/Linux system, if you are on Windows they
*should* work but I can't make any promises.

```bash
git clone https://github.com/mcbarlowe/NHLcsscrape.git
cd NHLcsscrape
pip install requirements.txt
python nhlcsscrape.py file_name
```
`file_name` will be the name you want the pipe delimited output
file to be called. If you have any problems or questions feel free
to email me or contact me on twitter [@matt_barlowe](https://twitter.com/matt_barlowe).
Hope you enjoy!
