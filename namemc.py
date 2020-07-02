import requests
import sys
import time
import argparse
from bs4 import BeautifulSoup
import re


parser = argparse.ArgumentParser()
parser.add_argument('inFile', type=str, help='Input text file for names')
parser.add_argument('outFile', type=str, help='Output text file for names')
parser.add_argument('-w', '--wait', nargs='?', help='Time between requests in seconds, default 1', const=1, type=float, default=1)
parser.add_argument('-c', '--cooldown', nargs="?", help='Time between request after error in seconds, default 5', const=1, type=float, default=5)
parser.add_argument('-b', '--nowritebad', help='Disables writing of usernames to file that arent available', action='store_true')
parser.add_argument('-s', '--nowritesoon', help='Disables writing of usernames to file that are available soon', action='store_true')
parser.add_argument('-p', '--print', help='Disables console printing', action='store_true')
args = parser.parse_args()
indir = args.inFile
outdir = args.outFile
cooldown = args.cooldown
wait = args.wait
nowritesoon = args.nowritesoon
nowrite = args.nowritebad
printing = args.print


def testName(name):
	url = "https://namemc.com/search?q=" + name
	response = requests.get(url)
	if "<div id=\"status-bar\" class=\"card bg-success text-white\">" in response.text:
		return "available now"
	if "<div id=\"status-bar\" class=\"card bg-info text-white\">" in response.text:
		s = response.text
		start = "<time id=\"availability-time\" class=\"text-nowrap\" datetime=\""
		end = "Z\">"
		result = re.search(start+"(.*)"+end, s)
		return "available on " + result.group(1).replace("T", " at ")[:-4] + " UTC"
	if "<div id=\"status-bar\" class=\"card bg-warning text-black\">" in response.text:
		return "taken"
	if "<div id=\"status-bar\" class=\"card bg-danger text-white\">" in response.text:
		return "bad characters"
	return "error"


outFile = open(outdir, "a")
inFile = open(indir, "r")
with inFile as a_file:
	for line in a_file:
		stripped_line = line.strip()
		if stripped_line != "":
			status = testName(stripped_line)
			if status == "error":
				while status == "error":
					if not printing:
						print("error waiting "+ str(cooldown) +" seconds and trying again")
					time.sleep(cooldown)
					status = testName(stripped_line)
			if status != "taken" and status != "error":
				if not printing:
					print("------------" + stripped_line + " is " + status + "------------")
				if( ("now" not in status and not nowritesoon) or ("now" in status)):
					outFile.write(stripped_line + " is " + status + "\n")
			elif status == "taken": 
				if not printing:
					print(stripped_line + " is " + status)
				if(not nowrite):
					outFile.write(stripped_line + " is " + status + "\n")
			time.sleep(wait)
inFile.close()
outFile.close()