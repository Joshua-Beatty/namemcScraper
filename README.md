# namemcScraper
Scrapes namemc based off a list of usernames and writes details to a file

## Usage
```
namemc.py [-h] [-w [WAIT]] [-c [COOLDOWN]] [-b] [-s] [-p] inFile outFile

positional arguments:
  inFile                Input text file for names
  outFile               Output text file for names

optional arguments:
  -h, --help            show this help message and exit
  -w [WAIT], --wait [WAIT]
                        Time between requests in seconds, default 1
  -c [COOLDOWN], --cooldown [COOLDOWN]
                        Time between request after error in seconds, default 5
  -b, --nowritebad      Disables writing of usernames to file that arent available
  -s, --nowritesoon     Disables writing of usernames to file that are available soon
  -p, --print           Disables console printing
```
### Example
Given a file `names.txt`
```
name1
hello!
asdasdafsdsda
fdsfdssas
why?
no
35iq
 ```
 The command `python namemc.py names.txt out.txt`
 generates the file `out.txt`
 ```
name1 is taken
hello! is bad characters
asdasdafsdsda is available now
fdsfdssas is available now
why is taken
no is bad characters
35iq is available on 2020-07-03 at 06:15:39 UTC
```

## Gotchas
The program automatically strips any '?' from a name before testing to avoid an error in loading the page
 
