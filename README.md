# DMFlashScore

DMFlashScore is a Python based program dealing with graphical presentation of statistical data extracted from Flashscore website https://www.flashscore.com/
It scrapes the information for the Premier League such as:
- premier league teams
- standings information of the 5 previous seasons
- matches and goals between teams
- form of last 5 matches
- players of each team and their stats

## Installation

Get the code on https://github.com/aroguerra/DMFlashscore/tree/master
Either download the zip folder and extract it or clone the repository into your computer

## Usage

The DMFlashScore has a CLI based user interface.
By running the command
```bash
./DMFlashScore.py main.py *command*
```
 command | action |
|--------------|-------------------------------|
| -h, --help   | show this help message and exit |
| -all, -a     | fetch all scraped data        |
| -seasons, -s | fetch last 5 seasons data     |
| -matches, -m | fetch all scraped data        |
| -players, -p | fetch players data            |
| -form, -f    | fetch form last 5 matches data |
| -teams, -t   | fetch teams data              |

This command will activate scrapping based data mining process and save the scrapped data into a mysql database.
The Database will create the tables:

| Tables_in_flashscore   |
|------------------------|
| form_last_five_matches |
| matches                |
| players                |
| standings_five_seasons |
| teams                  |



## Description

DMFlashScore is a [Selenium](https://pypi.org/project/selenium/) based data mining application, which scrapes statistical data from the Flashscore API and visually presents it to the potential gambler. While the request and grequest Python modules are used in this application to access the webpages, the Selenium Python module is used to fined and fetch relevant data objects. The presentation of the data is done by a ReDash created dashboard, and the user interface is CLI based.